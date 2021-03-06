#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
get content from http://company.g0v.ronny.tw/api/show/公司統編

P.S: encooding in env must be UTF-8
"""

import requests
from datetime import datetime
import json
import sys
import traceback
from time import sleep
import requests

import threading
from utils import get8DigitCompanyId
from utils import getTotalLineNumOfFile
from utils import get2DigitMonthOrDate
import os
import csv

class RonnyGovDataCrawler:
    def __init__(self, url, inputFileName, outputFileName):
        self.inputFileName=inputFileName
        self.outputFileName=outputFileName
        self.url=url
    def __skip_1_line(self):
        idx=0
        try:
            inputFile=open(self.inputFileName, mode='r', encoding='UTF-8')
            tmpFile=open(self.outputFileName+'_tmp', mode='w',encoding='UTF-8')
            for line in inputFile:
                if idx == 0:
                    idx=1
                else:
                    tmpFile.write(line)
            self.inputFileName=self.outputFileName+'_tmp'
        except IOError as e:
            traceback.print_exc()   
        finally:
            print('Skip the 1st line')
            inputFile.close()
            tmpFile.close()
            
        
    def parse(self, skip1stLine=False, delimiter=None, idFieldNo=0):
        totalLines=getTotalLineNumOfFile(self.inputFileName)
        successCount=0
        idx=0
        
        if skip1stLine:
            self.__skip_1_line()
        
        try: 
            inputFile=open(self.inputFileName, mode='r', encoding='UTF-8')
            outputFile=open(self.outputFileName, mode='w',encoding='UTF-8')
            errorFile=open(self.outputFileName+'_err', mode='w',encoding='UTF-8')

            for line in inputFile:
                company_status='' # 公司狀況
                company_name=''   # 公司名稱
                company_capital='' # 資本總額(元)
                company_real_capital='' #實收資本額(元)
                company_respnsible_person=''  # 代表人(負責人)姓名
                company_addr='' # 公司所在地
                registry_unit='' # 登記機關
                registry_date='' # 核准設立日期
                change_date='' # 最後核准變更日期
                company_type=''

                if delimiter == None:
                    company_id=get8DigitCompanyId(line.strip())
                else:
                    company_id=line.split(delimiter)[idFieldNo]
                    
                try:
                    r=requests.get(self.url+'/'+company_id)
                    jsonOutput=r.json()
                    #print(jsonOutput)
                    print('Processing records: '+str(idx)+'/Total records: '+str(totalLines))
                    if 'data' in jsonOutput:
                        if '公司狀況' in jsonOutput['data']:
                            company_status=jsonOutput['data']['公司狀況']
                        elif '分公司狀況' in jsonOutput['data']:
                            company_status=jsonOutput['data']['分公司狀況']
                        if '公司名稱' in jsonOutput['data']:
                            #print(jsonOutput['data']['公司名稱'])
                            if type(jsonOutput['data']['公司名稱']) is str:
                                company_name=jsonOutput['data']['公司名稱'].strip()
                            elif type(jsonOutput['data']['公司名稱'][0]) is str:
                                company_name=jsonOutput['data']['公司名稱'][0].strip()
                            else:
                                company_name=jsonOutput['data']['公司名稱'][0][0].strip()
                           # print(company_name)
                            company_type='公司'
                        elif '分公司名稱' in jsonOutput['data'] and '財政部' in jsonOutput['data'] and '營業人名稱' in jsonOutput['data']['財政部']:
                            #print(jsonOutput['data']['公司名稱'])
                            company_name=jsonOutput['data']['財政部']['營業人名稱'].strip()
                           # print(company_name)
                            company_type='分公司'
                        if '資本總額(元)' in jsonOutput['data']:
                            company_capital=jsonOutput['data']['資本總額(元)'].replace(',','')
                        if '實收資本額(元)' in jsonOutput['data']:
                            company_real_capital=jsonOutput['data']['實收資本額(元)'].replace(',','')
                        if '代表人姓名' in jsonOutput['data']:
                            company_respnsible_person=jsonOutput['data']['代表人姓名']
                        elif '訴訟及非訴訟代理人姓名' in jsonOutput['data']:
                            if type(jsonOutput['data']['訴訟及非訴訟代理人姓名']) is str:
                                company_respnsible_person=jsonOutput['data']['訴訟及非訴訟代理人姓名']
                            else:
                                company_respnsible_person=jsonOutput['data']['訴訟及非訴訟代理人姓名'][0]
                       # elif '分公司經理姓名' in jsonOutput['data']:
                       #     if type(jsonOutput['data']['分公司經理姓名']) is str:
                       #         company_respnsible_person=jsonOutput['data']['分公司經理姓名']
                       #     else:
                       #         company_respnsible_person=jsonOutput['data']['分公司經理姓名'][0]
                        if '公司所在地' in jsonOutput['data']:
                            company_addr=jsonOutput['data']['公司所在地']
                        elif '分公司所在地' in jsonOutput['data']:
                            company_addr=jsonOutput['data']['分公司所在地'].strip()
                            company_type='分公司'

                        if '登記機關' in jsonOutput['data']:
                            registry_unit=jsonOutput['data']['登記機關']
                        if '核准設立日期' in jsonOutput['data'] and jsonOutput['data']['核准設立日期' ]!=None:
                            registry_date=str(jsonOutput['data']['核准設立日期']['year'])+get2DigitMonthOrDate(str(jsonOutput['data']['核准設立日期']['month']))+get2DigitMonthOrDate(str(jsonOutput['data']['核准設立日期']['day']))
                        if '最後核准變更日期' in jsonOutput['data'] and jsonOutput['data']['最後核准變更日期' ]!=None:
                            change_date=str(jsonOutput['data']['最後核准變更日期']['year'])+get2DigitMonthOrDate(str(jsonOutput['data']['最後核准變更日期']['month']))+get2DigitMonthOrDate(str(jsonOutput['data']['最後核准變更日期']['day']))
                        
                        if '商業名稱' in jsonOutput['data']:
                            company_name=jsonOutput['data']['商業名稱']
                            company_type='商業'
                        if '現況' in jsonOutput['data']:
                            company_status=jsonOutput['data']['現況']
                        if '資本額(元)' in jsonOutput['data']:
                            company_capital=jsonOutput['data']['資本額(元)'].replace(',','')
                        if '負責人姓名' in jsonOutput['data']:
                            company_respnsible_person=jsonOutput['data']['負責人姓名']
                        if '地址' in jsonOutput['data']:
                            company_addr=jsonOutput['data']['地址']
                        if '最近異動日期' in jsonOutput['data'] and jsonOutput['data']['最近異動日期' ]!=None:
                            change_date=str(jsonOutput['data']['最近異動日期']['year'])+get2DigitMonthOrDate(str(jsonOutput['data']['最近異動日期']['month']))+get2DigitMonthOrDate(str(jsonOutput['data']['最近異動日期']['day']))
                        
                        # print(company_status) # 公司狀況
                        # print(company_name)   # 公司名稱
                        # print(company_capital) # 資本總額(元)
                        # print(company_real_capital) #實收資本額(元)
                        # print(company_respnsible_person)  # 代表人(負責人)姓名
                        # print(company_addr) # 公司所在地
                        # print(registry_unit) # 登記機關
                        # print(registry_date) # 核准設立日期
                        # print(change_date) # 最後核准變更日期
                        # print(company_type)
                        outputFile.write('"'+company_id+'","'+company_status+'","'+company_name+'","'+company_type+'","'
                            +company_capital+'","'+
                            company_real_capital+'","'+
                            company_respnsible_person+'","'
                            +company_addr+'","'+
                            registry_unit+'","'+
                            registry_date+'","'+
                            change_date+'"'+'\n')
                        successCount+=1
                    else:
                        errorFile.write(company_id+',2'+'\n') 
                    #print(jsonOutput)
                except Exception as e:
                    traceback.print_exc() 
                    errorFile.write(company_id+',1'+'\n') 
                finally:
                    idx+=1

                    

        except IOError as e:
            traceback.print_exc()   
        finally:
            print('Successful records: '+ str(successCount) +'/Total records: '+str(totalLines))
            inputFile.close()
            outputFile.close()
            errorFile.close()

def str2bool(v):
    return v.lower() in ("YES, ""yes", "true", "t", "1", "True", "TRUE")
if __name__ == '__main__':
   # sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
   # inputFileName='/Users/sary357/Downloads/work.csv'
   # inputFileName='D:/fuming.Tsai/Documents/Tools/PortableGit/projects/GitDocs/06-專案文件/05-SME授信客戶資金需求/parse_again.txt'
   # outputFileName='/Users/sary357/Downloads/work_output.csv'
   # outputFileName='D:/fuming.Tsai/Documents/Tools/PortableGit/projects/GitDocs/06-專案文件/05-SME授信客戶資金需求/id_out.csv'
    url='http://company.g0v.ronny.tw/api/show'
    today=datetime.now()
    
    fmt = '%Y-%m-%d %H:%M:%S'
    print('Starting time: '+ today.strftime(fmt))


    if len(sys.argv) < 3:
        print(sys.argv[0] + ' INPUT_FILE OUTPUT_FILE' )
        print(sys.argv[0] + ' INPUT_FILE OUTPUT_FILE [true|false] ' )
        print(sys.argv[0] + ' INPUT_FILE OUTPUT_FILE [true|false] "," 0 ' )
    else:
        # (self, skip1stLine=False, delimiter=None, idFieldNo=0)
        print("Start to Process...")
        
        inputFileName=sys.argv[1]
        outputFileName=sys.argv[2]
        crawler=RonnyGovDataCrawler(url,inputFileName, outputFileName)
        if len(sys.argv) == 3:
            crawler.parse()
        else:
            skipOrNot=str2bool(sys.argv[3])
            delimiter=None
            fieldNo=0
            if len(sys.argv) >=5:
                delimiter=sys.argv[4]
                fieldNo=int(sys.argv[5])
            crawler.parse(skipOrNot, delimiter, fieldNo)
    today=datetime.now()
    print('End time: '+ today.strftime(fmt))

   
