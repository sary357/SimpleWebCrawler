# FindbizCrawler.py: get data from 商工公示(http://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do)
## how to use this script
1. modify the following according to your env
```
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
```
2. execute this script
```
$ python FindbizCrawler.py
```
# RonnyGovDataCrawler.py: get the data from http://company.g0v.ronny.tw/
## how to use this script
1. modify the following according to your env
```
if __name__ == '__main__':
   # sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    inputFileName='/Users/sary357/Downloads/work.csv'
    
    outputFileName='/Users/sary357/Downloads/work_output.csv'
    
    url='http://company.g0v.ronny.tw/api/show'
    today=datetime.now()
    
    fmt = '%Y-%m-%d %H:%M:%S'
    print('Starting time: '+ today.strftime(fmt))

    crawler=RonnyGovDataCrawler(url,inputFileName, outputFileName)
    crawler.parse()

    today=datetime.now()
    print('End time: '+ today.strftime(fmt))
```
2. execute this script
```
$ python RonnyGovDataCrawler.py
```
# Todo items
1. 中華黃頁(https://www.iyp.com.tw/)
2. ForeignTradeData (國貿局進出口廠商管理系統: https://fbfh.trade.gov.tw/rich/text/indexfbOL.asp)
