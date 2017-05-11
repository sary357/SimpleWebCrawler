#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
base class of web crawler

P.S: encodoing in env must be UTF-8
"""


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
from lxml import etree
import time
import random

class BaseWebCrawler(threading.Thread):
    def __init__(self, threadID, isSessionOn, isGet, isPost, url, keyFieldName, timeout, paramsDicArray, outputFile=None,**headers):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.session=requests.Session()
        self.sessionOn=isSessionOn
        self.isPost=isPost
        self.isGet=isGet
        self.content=None
        self.url=url
        self.keyFieldName=keyFieldName
        self.timeout=timeout
        self.paramsDicArray=paramsDicArray
        self.headers=headers['headers']
        self.content={}
        self.outputFile=outputFile
    def closeSession(self):
        if self.sessionOn:
            self.session.close()
    def run(self):
        self.content={}
        idx=0
        totalLineNumOfFile=len(self.paramsDicArray)
        print('ThreadID: '+ str(self.threadID) + " is processing the URL: " + self.url)
        
        if self.outputFile != None:
            outputFilePtr=open(self.outputFile, mode='w')
        
        if self.paramsDicArray != None:
            for idx in range(0, len(self.paramsDicArray)):
                print('Thread ID: %d/Processing # of records: %d/Total # of records: %d'%(self.threadID,idx+1, totalLineNumOfFile))
                c=None

                keyFieldValue=self.paramsDicArray[idx][self.keyFieldName]
                #print('gggg:'+str(self.headers))
                sleepTime=random.randint(1, 10)
                time.sleep(sleepTime)
                try:
                    if self.sessionOn and self.isGet:
                        c=self.session.get(self.url, headers=self.headers, params=self.paramsDicArray[idx], timeout=self.timeout)
                    if  not self.sessionOn and self.isGet:
                        c=requests.get(self.url, headers=self.headers, params=self.paramsDicArray[idx], timeout=self.timeout)
                    if self.sessionOn and self.isPost:
                        c=self.session.post(self.url, headers=self.headers, data=self.paramsDicArray[idx], timeout=self.timeout)
                    if not self.sessionOn and self.isPost:
                        c=requests.post(self.url, headers=self.headers, data=self.paramsDicArray[idx], timeout=self.timeout)
                    
                except Exception as e:
                    print('url:',self.url)
                    print('headers:',self.headers)
                    print('params:', self.paramsDicArray[idx])
                    traceback.print_exc()
                finally:
                    if c != None:
                        if self.outputFile  == None:
                            self.content[keyFieldValue]=c.text
                        else:
                            #print(c.text)
                            # outputFilePtr.write(keyFieldValue+','+c.text)
                            #print(c.text)
                            page=etree.HTML(c.text)
                            t=page.xpath(u"//div[contains(@class, 'panel-heading companyName')]/a[contains(@class,'hover')]/descendant::text()")[0]
                            restContent=''.join(page.xpath(u"//div[contains(@class, 'panel panel-default')]/div[contains(@class,'panel-body')]/descendant::text()")).replace('\t','').replace('\n','').replace('\xa0','')
                            restContentArray=restContent.split(',')
                            # last Element:'詳細資料'
                            tmpResultArray=[]
                            cidx=0
                            stopInput=False
                            #print(restContentArray)
                            while cidx < len(restContentArray) and stopInput==False:
                                #print(restContentArray[cidx])

                                tmpStrArr=restContentArray[cidx].split(':')
                                
                                
                                if '詳細資料' in tmpStrArr[1]:
                                    stopInput=True
                                    tmpResultArray.append(tmpStrArr[1].split('詳細資料')[0].strip())
                                else:
                                    tmpResultArray.append(tmpStrArr[1].strip())
                                cidx+=1
                                
                            outputFilePtr.write(keyFieldValue+','+str(t)+','+','.join(tmpResultArray)+'\n')
                    else:
                        if self.outputFile  == None:
                            self.content[keyFieldValue]=None
                        else:
                            outputFilePtr.write(keyFieldValue+','+'\n')
                   #print(self.content[keyFieldValue])
        else:
            try:
                if self.sessionOn and self.isGet:
                    c=self.session.get(self.url, headers=self.headers, timeout=self.timeout)
                if not self.sessionOn and self.isGet:
                    c=requests.get(self.url, headers=self.headers, timeout=self.timeout)
                if self.sessionOn and self.isPost:
                    c=self.session.post(self.url, headers=self.headers, timeout=self.timeout)
                if not self.sessionOn and self.isPost:
                    c=requests.post(self.url, headers=self.headers, timeout=self.timeout)
                    
            except Exception as e:
                print('url:',url)
                print('headers:',headers)

                traceback.print_exc()
            finally:
                if c != None:
                    if self.outputFile  == None:
                        self.content[keyFieldValue]=c.text
                    else:
                        # outputFilePtr.write(keyFieldValue+','+c.text)
                        page=etree.HTML(c.text)
                        t=page.xpath(u"//div[contains(@class, 'panel-heading companyName')]/a[contains(@class,'hover')]/descendant::text()")
                        restContent=''.join(page.xpath(u"//div[contains(@class, 'panel panel-default')]/div[contains(@class,'panel-body')]/descendant::text()")).replace('詳細資料','').replace('\t','').replace('\n','').replace('\xa0','')
                        restContentArray=restContent.split(',')
                        tmpResultArray=[]
                        cidx=0
                        for cidx in range(0, len(restContentArray)):
                            #print(restContentArray[cidx])
                            tmpResultArray.append(restContentArray[cidx].split(':')[1].strip())
                            
                        outputFilePtr.write(keyFieldValue+','+str(t[0])+','+','.join(tmpResultArray)+'\n')
                else:
                    if self.outputFile  == None:
                        self.content[keyFieldValue]=None
                    else:
                        outputFilePtr.write(keyFieldValue+','+'\n')
        self.closeSession()
        if self.outputFile != None:
            print('Dump the result to file: '+ self.outputFile)

    def getContent(self):
        #print(self.content)
        return self.content