import sys
import re
import os
sys.path.append(r'C:\Users\22222\pythonScripts\Factory')
from omega_db import *
from omega_ye import *


class YE2DB_Extractor():
    def __init__(self,path=os.getcwd()):
        self._SummaryDB = omega_db()
        self._TBBinningDB = omega_db()
        self._yeParser = omega_ye()
        self._path = path
        self._defaultSummaryDBName = 'Summary.db'
        self._defaultTBBiningDBName = 'Binning.db'
        self._TABLENAME_STSum = {
            '.1st':'ST_1st',
            '.rescreen':'ST_resreen',
            }
        self._BINNING_KEY = slice(1,9)
        self._BINNING_STEP = 3
    def _initDB(self, dbName=None):
        self._SummaryDB.connectDB(self._defaultSummaryDBName)
        self._TBBinningDB.connectDB(self._defaultTBBiningDBName)
        self._SummaryDB.createTable(self._TABLENAME_STSum['.1st'],'filename TEXT NOT NULL, enddate TEXT, step TEXT,lot TEXT, device TEXT, pgm TEXT, cnefw TEXT, avgTT REAL, tester TEXT, temp INTEGER, yield TEXT, inQty INTEGER, outQty INTEGER, bin2 INTEGER, bin3 INTEGER, bin4 INTEGER, bin5 INTEGER, bin6 INTEGER, bin7 INTEGER, bin8 INTEGER, rescreen TEXT, fw TEXT, parmfile TEXT, efusefile TEXT, formatlba INTEGER, maxlba INTEGER, PRIMARY KEY(filename)')
        self._SummaryDB.createTable(self._TABLENAME_STSum['.rescreen'],'filename TEXT NOT NULL, enddate TEXT, step TEXT,lot TEXT, device TEXT, pgm TEXT, cnefw TEXT, avgTT REAL, tester TEXT, temp INTEGER, yield TEXT, inQty INTEGER, outQty INTEGER, bin2 INTEGER, bin3 INTEGER, bin4 INTEGER, bin5 INTEGER, bin6 INTEGER, bin7 INTEGER, bin8 INTEGER, rescreen TEXT, fw TEXT, parmfile TEXT, efusefile TEXT, formatlba INTEGER, maxlba INTEGER, PRIMARY KEY(filename)')
    
    def extract(self,arg='.*'):
        self._initDB()
        for filename in [f for f in os.listdir(self._path) if f.endswith( ('.1st','.rescreen') ) and re.search(arg,f) is not None]:
            print('File: {:<s}'.format(filename))
            tableName = [self._TABLENAME_STSum[x] for x in self._TABLENAME_STSum.keys() if x in filename].pop()
            if self._SummaryDB.isNotInDB(tableName,'filename', filename):
                print('Insert %s into database...' % filename)
                for datalist in self._yeParser.handleData(os.path.join(self._path,filename)):
                    if datalist[0] == 'SUMMARY':
                        self._SummaryDB.insertDataIntoTable(tableName, datalist[1:])
                    elif datalist[0] == 'BINNING':
                        if '0xffffffff' not in datalist[-1]:
                            softbin = datalist[-1]
                            softbin = softbin[:softbin.find(':')]
                            if '0001' not in softbin:
                                key = ','.join(datalist[self._BINNING_KEY])
                                binning_tableName = None
                                if filename.endswith('.1st'):
                                    binning_tableName = '_'.join([str(datalist[self._BINNING_STEP]),'1st',str(softbin)])
                                elif filename.endswith('.rescreen'):
                                    binning_tableName = '_'.join([str(datalist[self._BINNING_STEP]),'rescreen',str(softbin)])
                                self._TBBinningDB.createTable(binning_tableName,'binning_key TEXT NOT NULL, binning TEXT, PRIMARY KEY(binning_key)')
                                self._TBBinningDB.insertDataIntoTable(binning_tableName,[key,softbin])
            self._saveDB()
        self._closeDB()
    def _saveDB(self):
        self._SummaryDB.saveDB()
        self._TBBinningDB.saveDB()
    def _closeDB(self):
        self._SummaryDB.closeDB()
        self._TBBinningDB.closeDB()        
    def _saveAndCloseDB(self):
        # save and close DB
        self._SummaryDB.saveDB()
        self._TBBinningDB.saveDB()
        self._SummaryDB.closeDB()
        self._TBBinningDB.closeDB()
        print('database updated')        



if len(sys.argv) > 1: # user has input extra argument for searching specific files
    for arg in sys.argv[1:]:
        YE2DB_Extractor(os.getcwd()).extract(arg)
else:
    YE2DB_Extractor(os.getcwd()).extract()
