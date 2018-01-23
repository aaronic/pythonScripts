import os
import re
import sys

"""
datalogParser handle the basic function/variable

"""
class omega_datalog(object): # super() can be only used for class which is the subclass of 'object', otherwise, the subclass of this class will have TypeError: must be type, not classobj
    def __init__(self, testerType):
        self._currentPath = os.getcwd()
        self._testerType = testerType # '5831'/'5773'
        self._files = []
        self._specialFilename = None
        self._fileParsed = ''
        self._dutInfo = {}
        self._tbIsStarted = False
        self._testIsStarted = False
        self._touchdown = 0
        self._dataline = ''
        self._currentTBName = None
        self._currentTBTT = None
        self._specialTBList = None
        self._isDCData = False
        self._keyWords = {
            'TBSTART': 'TestBlock = ',
            'TBEND': '	TestItem:',
            'TESTSTART': 'Start_of_Test -----',
            'TESTEND': 'Execution time:',
            'DCTEST':'(PIN|VS)[0-9]{1,2}\s+DUT[0-9]{1,2}',
            'SEEKING':'^Now seeking:'
            }
        self._dutInfo = {}
        self._tbInfo = {} # ley->self._fileParsed,self._touchdown,self._dut
        self._tbList = []
        
    # clean up variables for each file
    def _cleanVariables(self):
        self._touchdown = 0
        self._testIsStarted = False
        self._tbIsStarted = False
        self._dutInfo = {}
        self._dataline = ''
        self._currentTBName = None
        self._currentTBTT = None

    # collect the datalog files under the current path    
    def _collectFiles(self):
        tmpFiles = os.listdir(self._currentPath)
        for self._fileParsed in tmpFiles:
            if self._specialFilename is None:
                yield self._fileParsed
            elif self._specialFilename in self._fileParsed:
                yield self._fileParsed

    # identify the filename of 5773 or 5831.           
    def _updateSpecialFilename(self):
        if self._testerType == '5831':
            self._specialFilename = 'fsdiag'
        elif self._testerType == '5773':
            self._specialFilename = 'kei'

    # yield every line data        
    def _yieldDataline(self):
        print('File: %s' % self._fileParsed)
        with open(self._fileParsed,'r') as fi:
            for line in fi.readlines():
                yield line
    # check if test start, connect DB if start, close DB if end
    def _checkTestStartOrEnd(self):
        if re.search(self._keyWords['TESTSTART'],self._dataline) is not None:
            self._touchdown += 1
            self._testIsStarted = True
            self._datalogDB.connectDB('tmpDB.db')
        elif re.search(self._keyWords['TESTEND'], self._dataline) is not None:
            self._testIsStarted = False
            self._datalogDB.closeDB()
    # check if test block start, get tb name and create the table named as tb        
    def _checkTestBlockStartOrEnd(self):
        if re.search(self._keyWords['TBSTART'],self._dataline) is not None:
            self._tbIsStarted = True
            self._currentTBName = self._getTBName()
            self._datalogDB.createTable(self._currentTBName,'key TEXT NOT NULL PRIMARY KEY,data TEXT')
        elif re.search(self._keyWords['TBEND'], self._dataline) is not None:
            self._tbIsStarted = False
            self._currentTBTT = self._getTBTT()
            self._datalogDB.saveDB()           
    # check if the dataline is DC parametric data    
    def _checkParametricDataFlag(self):
        
        if re.search(self._keyWords['DCTEST'],self._dataline) is not None:
            #print('checking DC data')
            self._isDCData = True
            self._dut,self._pin,self._pinValue = self._getParametricData()
        else:
            self._isDCData = False
    # seek all test blocks in the datalog
    def _seekTestBlocks(self):
        def seekTB(data):
            datas = data.split()
            return datas[-1].strip()
        if re.search(self._keyWords['SEEKING'], self._dataline) is not None:
            tb = seekTB(self._dataline)
            if tb not in self._tbList:
                self._tbList.append(tb)
    # return all the test blocks from seeking results
    def getAllTBs(self):
        return self._tbList
    # get all files which need to be parsed    
    def getFiles(self):
        self._updateSpecialFilename()
        return self._collectFiles()
    # get current touchdown ID
    def getTouchdown(self):
        return self._touchdown
    # get current file for parsing
    def getParsedFile(self):
        return self._fileParsed
    # open the file for parsing and insert data to database
    def handleFiles(self, specialTBList=None):
        if specialTBList is not None:
            self._specialTBList = specialTBList # if user specify the test block
        for fi in self.getFiles(): # get the datalog file in the current path
            self._cleanVariables()
            for self._dataline in self._yieldDataline():
                tmp = self._handleDataline()
                if tmp is not None:
                    k,v = tmp
                    data = ','.join(self._datalogDB.adjustDataFormat(self._currentTBName,[k,v]))
                    if self._datalogDB.isNotInDB(self._currentTBName,'key',k):
                        self._datalogDB.insertDataIntoTable(self._currentTBName,data)
                    else: # append the data after
                        ori_datas = self._datalogDB.selectDataFromTable(self._currentTBName,'data',where=('key=\"%s\"' % k))
                        ori_data = ori_datas[0][0]
                        final_data = ','.join([ori_data,v])
                        print('Data already existed: %s' % final_data)
                        self._datalogDB.updateData(self._currentTBName,'data',final_data,'key',k)
                    
    ######### below function is overrided by subclass ###########
    # handle with each line data
    def _handleDataline(self):
        self._seekTestBlocks()
        self._checkTestStartOrEnd()
        self._checkTestBlockStartOrEnd() # record the current tb name and check if tb is started or end
        self._checkParametricDataFlag() # if it is the DC data, extract the data
        # realized by subclass
        # ....
    def _getTBName(self):
        pass
    def _getTBTT(self):
        pass
    def _getParametricData(self):
        # Sample:          -428.8mV  -200.0mV  -800.0mV   PIN12     DUT12
        # H-FAIL    120.4uA   100.0uA   2.000uA   VS1       DUT15    
        dataline = self._dataline.strip()
        datas = re.split('\s+',dataline)
        value,pin,dut = ['','','']
        if 'FAIL' in datas[0]: # fail pin
            value = datas[1]
        else:
            value = datas[0]
        pin,dut = [i for i in datas[-2:]]
        return str(dut),str(pin),str(value)
        
class omega_STDatalog(omega_datalog):
    def __init__(self, *args):
        super(STDatalogParser,self).__init__(*args)
        self._STTBKeyWords={
            'tb_CheckDuplicateCID':'CMD2 CID', # Tester: SD12	 Site: 73	 DUT[ 8]	 CMD2 CID #: 4501044413430363419d014f02c410
            'tb_sctpReadEFuseTest':'ControllerWaferXY:', # EFuse:  Get Four Bytes: ffffc32fControllerWaferXY:DUT20	9	36	46	154
            }

    def _getTBName(self):
        # Sample: TestBlock = tb_CheckST1Stamp :39014
        super(STDatalogParser,self)._getTBName()
        _,tbName,_ = re.split('[=:]',self._dataline)
        return tbName.strip()
    def _getTBTT(self):
        # 	TestItem:tb_CheckST1Stamp Test Time: 0.638[s]
        super(STDatalogParser,self)._getTBTT()
        _,_,tt,_ = re.split('[\[:]',self._dataline)
        return tt.strip()

    def _getTBData(self):
        if self._specialTBList is not None:
            if self._currentTBName in self._specialTBList:
                if self._isDCData:
                    #tmpkey = '.'.join([elf._fileParsed,self._touchdown,self._dut])
                    #self._tbInfo[tmpkey]={self._pin:self._pinValue}
                    return (','.join([self._fileParsed,str(self._touchdown),self._dut,self._pin]),self._pinValue)
                #if self._STTBKeyWords[self._currentTBName] in self._dataline:
                #    return self._dataline
                elif self._currentTBName in self._STTBKeyWords.keys():
                    if re.search(self._STTBKeyWords[self._currentTBName],self._dataline) is not None:
                        print(self._dataline)
            else:
                return None
        else:
            return (','.join([self._fileParsed,str(self._touchdown),self._dut]),self._dataline)
        
    def _handleDataline(self):
        super(STDatalogParser,self)._handleDataline()
        if self._testIsStarted and self._tbIsStarted:
            if self._getTBData() is not None:
                return self._getTBData()
            else:
                return None
        #if self._testIsStarted and not self._tbIsStarted:
        #    if self._currentTBName is not None and self._currentTBTT is not None and self._currentTBName in self._specialTBList:
        #        return 'tb:'+self._currentTBName+' tt:'+self._currentTBTT
        #    else:
        #        return None
        else:
            return None
        
        #if 'testStartAction' in self._dataline:
        #    print(self._dataline)
        #    print(self.getTouchdown())

    def getDBTables(self):
        self._datalogDB.connectDB('tmpDB.db')
        yield self._datalogDB.getAllTables()
        self._datalogDB.closeDB()

    def getDBTestBlocks(self, tbs):
        self._datalogDB.connectDB('tmpDB.db')
        for tb in tbs:
            print(tb)
            yield self._datalogDB.selectDataFromTable(tb,'*')
        self._datalogDB.closeDB()

tbs = ['tb_MaxV_VCC_Stdby_Current']        
dp = STDatalogParser('5773')

dp.handleFiles(tbs)
#for table in dp.getDBTables():
#    print(table)
#for tbinfo in dp.getDBTestBlocks(tbs):
#    print tbinfo
