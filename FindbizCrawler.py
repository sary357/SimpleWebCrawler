#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
商工登記公示資料
URL: http://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do

P.S: encooding in env must be UTF-8
"""

#from abc import ABCMeta, abstractmethod
#from http.client import HTTPConnection
#from http.client import HTTPException
#from urllib.parse import urlparse
from io import TextIOWrapper
from datetime import datetime
import json
import sys
import traceback
from time import sleep
import requests
import threading
from utils import splitFile
from utils import getTotalLineNumOfFile
import os
from BaseWebCrawler import BaseWebCrawler

# 統一編號: 01129166 , 
# 負責人: 陳中川 ,
# 登記機關: 臺北市商業處 , 
# 登記現況: 核准設立 , 
# 地址: 臺北市大同區錦西街53巷8號1樓 , 
# 資料種類: 商號 , 
# 核准設立日期: 1060307 , 
# 核准變更日期: 1060307

class FindbizCrawler():
    def __init__(self, sourceFileName, outputFileFolder, numThreads, *paramsDicArray):
        self.sourceFileName=sourceFileName
        self.outputFileFolder=outputFileFolder
        self.numThreads=numThreads
        self.url='http://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do'
        self.headers={'Referer':self.url}
        self.keyFieldName='qryCond'
        self.payload={'userResp': '', 'qryType': ['cmpyType', 'brCmpyType', 'busmType', ], 
        'busmType': 'true',  'infoDefault': 'true', 'cmpyType': 'true', 
        'infoType': ['infoDefault'], 'validatorOpen': 'N', 'isAlive': 'true', 
        'qryCond': 'qryCond', 'cPage': '', 'errorMsg': '', 'brCmpyType': 'true', 'rlPermit': '0'}

        self.contents=[]
# threadID, isSessionOn, isGet, isPost, url, keyFieldName, timeout=1, *paramsDicArray=None, **headers=None 
    def getContentAccordingCompanyId(self):
        idx=0
        paramsDicArray=[]
        threads=[]
        today=datetime.now().strftime("%Y%m%d%H%M%S")
        
        print('Start to process the file: '+ self.sourceFileName+' and output folder:'+self.outputFileFolder)
        try:

            totalLineNumOfFile=getTotalLineNumOfFile(self.sourceFileName)
            toBeProcessFileNames=splitFile(self.sourceFileName, os.path.dirname(self.sourceFileName), self.numThreads)
            #print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)
            #print(toBeProcessFileNames)

            toBeProcessArray=self.__processedPayload(toBeProcessFileNames, totalLineNumOfFile)
            idx=0
            for idx in range(0, self.numThreads):
                #print(toBeProcessArray[toBeProcessFileNames[idx]])

                threads.append(BaseWebCrawler(idx, True, False, True, self.url, self.keyFieldName, 1,
                    paramsDicArray=toBeProcessArray[toBeProcessFileNames[idx]] , headers=self.headers,outputFile=toBeProcessFileNames[idx].replace('.csv','_result.csv')))
                threads[idx].start()

            for idx in range(0, self.numThreads):
                threads[idx].join()


            # for idx in range(0,self.numThreads):
            #     tContent=threads[idx].getContent();
            #     for c in tContent:
            #         self.contents.append(c)
            #     print(tContent)
        except Exception as e:
            print('url:',self.url)
            print('headers:',self.headers)
            print('params:',self.payload)
            traceback.print_exc()
        
        # if self.contents!=None and len(self.contents)>0:
        #     outputFileName=self.outputFileFolder+'/'+'result_'+today+'.csv'
        #     try:
        #         f=open(outputFileName, mode='w')
        #         for c in self.contents:

        #             f.writelines(c)
        #         f.close()
        #     except Exception as e:
        #         print('Fail to write a output file: '+ (outputFileName))
        #         traceback.print_exc()
        #     finally:
        #         print('Finish to write a output file: '+outputFileName)




    def __processedPayload(self, toBeProcessFileNames, totalLineNumOfFile):
        paramsDicArray={}
        tmpList=[]
        #print(toBeProcessFileNames)
        for f in toBeProcessFileNames:
            tmpList=[]
            fContent=open(f, mode='r')
            for line in fContent:
                tmpPayload=self.payload.copy()
                tmpPayload[self.keyFieldName]=(line.strip())
                tmpList.append(tmpPayload)
            fContent.close()
            paramsDicArray[f]=tmpList
        #print(paramsDicArray)
        return paramsDicArray

if __name__ == '__main__':
   # sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    today=datetime.now()

    # source file path
    sourceFilePath='./'
    # source file name
    sourceFile='sampleFile.csv'
    # output file folder
    outputFileFolder='./'
    # num of threads
    numOfTheads=2
    findbizCrawler=FindbizCrawler(sourceFilePath+'/'+sourceFile, outputFileFolder, numOfTheads)
    findbizCrawler.getContentAccordingCompanyId()


    
