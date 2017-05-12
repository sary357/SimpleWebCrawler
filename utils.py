#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Some utilty functions

P.S: encodoing in env must be UTF-8
"""

import os

def splitFile(sourceFileName, tempOutFolder, numTempFiles):
    oFiles=[]
    oFileName=[]

    sourceFileNameOnly=os.path.basename(sourceFileName)
    try:
        ifile=open(sourceFileName, mode='r', buffering=-1, encoding='UTF-8')
        idx=0
        while idx < numTempFiles:
            ofile=open(tempOutFolder+"/"+sourceFileNameOnly+"_"+str(idx), mode='w')
            oFiles.append(ofile)
            oFileName.append(tempOutFolder+"/"+sourceFileNameOnly+"_"+str(idx))
            idx+=1

        idx=0
        for line in ifile:
            if idx==numTempFiles:
                idx=0
            stsLine=line.strip().replace('\ufeff','')
            if len(stsLine) < 8 and len(stsLine)>2:
                num="0"*(8-len(stsLine))
                stsLine=num + stsLine
            oFiles[idx].write(stsLine+'\n')
            idx+=1
    except Exception as e:
        raise
    finally:
        for f in oFiles:
            f.close()
        ifile.close()
    return oFileName



def get8DigitCompanyId(company_id):
    bao=company_id
    bao=bao.strip().replace('\ufeff','')
    if len(bao) <8:
        bao="0"*(8-len(bao))+bao
    return bao

def get2DigitMonthOrDate(monthOrDay):
    bao=monthOrDay
    bao=bao.strip().replace('\ufeff','')
    if len(bao) <2:
        bao="0"*(2-len(bao))+bao
    return bao

def getTotalLineNumOfFile(fileName):
    try:
        num_lines = sum(1 for line in open(fileName))
        return num_lines
    except Exception:
        raise
