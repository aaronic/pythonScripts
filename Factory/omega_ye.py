import os
import re
from collections import defaultdict
""" omega_ye
extract summary / log / test time / binning out from one YE file
return as data list for other scripts output to file or database
"""
class omega_ye:
    def __init__(self):
        self._filename = None
        self._dataType = None
        # summary var
        self._enddate = None
        self._device = None
        self._lot = None
        self._step = None
        self._pgm = None
        self._tester = None
        self._temperature = None
        self._avgTT = None
        self._die = None
        self._fw = None
        self._formatlba = None
        self._maxlba = None
        self._prmfile = None
        self._effile = None
        self._cnefw = None
        self._testerPlatform = None
        self._inQty = None
        self._outQty = None
        self._bin2Qty = None
        self._bin3Qty = None
        self._bin4Qty = None
        self._bin5Qty = None
        self._bin6Qty = None
        self._bin7Qty = None
        self._bin8Qty = None
        self._yield = None
        self._rescreen = None
        self._totalTT = None # only for MT
        self._touchdownCnt = None # only for MT
        self._isMT = False
        self._isSummary = False
        # test block var
        self._tbName = None
        self._touchdown = {}
        self._site = None
        self._dut = None
        self._dutData = None
        self._tbDataTracking = defaultdict(list) # in case we have multi test result in one tb, like wxy
        self._testTime = None
        
        
    def _debugPrint(self):
        print("FILE: %s\nEND DATE: %s\nDEVICE: %s\nLOT: %s\nStep: %s\nPGM: %s\nTESTER: %s" % (self._filename,self._enddate,self._device,self._lot,self._step,self._pgm,self._tester))
        print('TEMP: %s\nAVG TT: %s\nDIE: %s\nFW: %s\nFORMATLBA: %s\nMAXLBA: %s\nPRMFILE: %s' % (self._temperature,self._avgTT,self._die,self._fw,self._formatlba,self._maxlba,self._prmfile))
        print('EFFILE: %s\nCNE FW: %s\nIn Qty: %s\nOut Qty: %s\nYield: %s\nBIN: %s,%s,%s,%s,%s,%s,%s' %(self._effile,self._cnefw,self._inQty,self._outQty,self._yield,self._bin2Qty,self._bin3Qty,self._bin4Qty,self._bin5Qty,self._bin6Qty,self._bin7Qty,self._bin8Qty))
    ##################################################################################################
    # yield out data structure
    # self._IsSummary for user detect data type, if it is summary part or test block part, so they can do different handling based on data type
    def _returnSTData(self):
        return [
            self._dataType, self._filename,self._enddate,self._step,self._lot,self._device,
            self._pgm,self._cnefw,self._avgTT,self._tester,self._temperature,
            self._yield,self._inQty,self._outQty,self._bin2Qty,self._bin3Qty,
            self._bin4Qty,self._bin5Qty,self._bin6Qty,self._bin7Qty,self._bin8Qty,
            self._rescreen,self._fw,self._prmfile,self._effile,self._formatlba,self._maxlba,
            ]
    def _returnMTData(self):
        return [
            self._dataType, self._filename,self._enddate,self._step,self._lot,self._device,
            self._pgm,self._totalTT,self._tester,self._temperature,
            self._yield,self._inQty,self._outQty,self._bin2Qty,self._bin3Qty,
            self._bin4Qty,self._bin5Qty,self._bin6Qty,self._bin7Qty,self._bin8Qty,
            self._rescreen,self._touchdown,
            ]
    def _returnTBData(self):
        return [
            self._dataType, self._filename, self._lot, self._step, self._pgm,
            self._device,self._tbName, str(self._touchdown[self._site]),
            self._site, self._dut, ','.join(self._dutData),
            ]
    def _returnTBTT(self):
        return [
            self._dataType, self._filename, self._lot, self._step, self._pgm,
            self._device, self._tbName, self._testTime,
            ]
    def _returnBinningData(self):
        return [
            self._dataType, self._filename, self._lot, self._step, self._pgm,
            self._device, str(self._touchdown[self._site]),
            self._site, self._dut, self._dutData,
            ]
    ######################################################################################################
    # parse the filename and get time/step/lot/pgm directly
    def parseFilename(self, filename):
        self._filename = filename
        datalist = []
        self._rescreen = filename[filename.rfind('.')+1:]
        if filename.startswith('STData'): # ST summary
            self._isMT = False
            filename = filename[:filename.rfind('.')]
            time = filename[filename.rfind('_')+1:]
            filename = filename[:filename.rfind('_')]
            step = filename[filename.rfind('_')+1:]
            filename = filename[:filename.rfind('_')]
            lot = filename[filename.rfind('_')+1:]
            filename = filename[:filename.rfind('_')]
            pgm = filename[filename.find('_')+1:]
            datalist = [pgm, lot, step, time, self._rescreen]
        else:
            self._isMT = True
            filename = filename[:filename.rfind('.')]
            time = filename[filename.rfind('_')+1:]
            filename = filename[:filename.rfind('_')]
            step = filename[filename.rfind('_')+1:]
            filename = filename[:filename.rfind('_')]
            lot = filename[filename.rfind('_')+1:]
            datalist = [lot,step,time,self._rescreen]
        return datalist
            

    # determine if it is summary part/test block part/test time part/binning part
    def _dataIsSummary(self, dataline):
        if not self._isSummary: # not summary
            if 'sandisk summary report' in dataline.lower():
                self._isSummary = True
                self._dataType = 'SUMMARY'
            elif 'tbtesttime:' in dataline.lower():
                self._dataType = 'TESTTIME'
            elif 'bin:dut' in dataline.lower():
                self._dataType = 'BINNING'
            else:
                self._dataType = 'TESTBLOCKDATA'
        else: # is summary
            if 'end of summary' in dataline.lower():
                self._isSummary = False

        return self._isSummary
            
    # collect test block data
    def _collectTestBlockData(self, dataline):
        
        def getTBName(data):
            return data[data.find(':')+1:]

        def getSite(data):
            return 'site'+data[data.find(':')+1:]

        def getTestTime(data):
            return data[data.find(':')+1:]

        def getDutData(data):
            def formatDut(dut):
                dut = dut.lower()
                if len(dut) == 4: # dut4 -> dut04
                    dut = dut[:dut.find('t')+1]+'0'+dut[dut.find('t')+1:]
                return dut.lower()          
            datalist =  re.split('[\s\t]+',data)
            dut = datalist[0]
            dut = dut[dut.find(':')+1:]
            dut = formatDut(dut)
            data = ':'.join(datalist[1:])
            return (dut,data)
            
    
        data = dataline.strip('\n')
        
        # TB:tb_ContactAll
        if 'TB:' in data: # test block name
            self._tbName = getTBName(data)
            self._tbDataTracking.clear() # clear the tb Data tracking hash
        #   accept -> SITE:1
        #   exclude -> DUTS_PER_SITE:16
        if 'SITE:' in data and '_SITE:' not in data:
            self._site = getSite(data)
            if self._site not in self._touchdown.keys():
                self._touchdown[self._site] = 0
            else:
                self._touchdown[self._site] += 1
        # OPEN:Dut01	D00         	00267.300018	mV
        if ':dut' in data.lower():
            self._dut,self._dutData = getDutData(data)
            if 'bin:dut' not in data.lower(): # not handle the binning data 
                self._tbDataTracking[self._dut].append(self._dutData)
            else:
                pass
        else:
            self._dut,self._dutData = (None,None)

        # TBTestTime:4.652
        if 'tbtesttime:' in data.lower():
            self._testTime = getTestTime(data)
        
    # extract summary data info, just one data line       
    def _collectSummaryData(self, dataline):
        def extract2ndColdata(data):
            data = data.strip()
            return data[data.rfind('=')+1:].strip()
        def extract1stColdata(data):
            data = data.strip()
            datalist = re.split('=',data)
            datalist2 = re.split('\s+',datalist[1])
            return datalist2[1].strip()
        def extractQty(data):
            data = data.strip() # there is a space in front of 'TOTAL' in adv, but no space in shracku
            datalist = re.split('\s+',data)
            return datalist[1:]
            
        data = dataline.strip('\n')
        if '  END  ' in data: # END date
            self._enddate = extract2ndColdata(data)
        if 'DEVICE#' in data: # device
            self._device = extract2ndColdata(data)
        if 'LOT#' in data: # lot
            self._lot = extract1stColdata(data)
        if 'OPN ' in data: # step
            self._step = extract1stColdata(data)
        if 'PGM ' in data: # ST program
            self._pgm = extract1stColdata(data)
        if 'TESTER#' in data: # tester
            self._tester = extract1stColdata(data)
        if 'TEMP ' in data: # temperature
            self._temperature = extract2ndColdata(data)
        if 'AverageTT' in data: # average TT
            if self._testerPlatform is 'shracku':
                self._avgTT = extract1stColdata(data)
            else:
                self._avgTT = extract2ndColdata(data)
        if 'DIECOUNT' in data: # diecount
            self._die = extract2ndColdata(data)
        if 'FORMATLBA' in data: # format lba
            self._formatlba = extract1stColdata(data)
        if 'MAXLBA' in data: # maxlba
            self._maxlba = extract2ndColdata(data)
        if 'PRMFILE' in data: # parameter file
            self._prmfile = extract2ndColdata(data)
        if 'EFFILE' in data: # efuse file
            self._effile = extract1stColdata(data)
        if 'CNE FW' in data: # cne fw
            self._cnefw = extract1stColdata(data)
        if data.startswith(' FW ') or data.startswith('FW '):
            self._fw = extract1stColdata(data)
        if data.startswith(' TOTAL') or data.startswith('TOTAL'):
            self._outQty,self._bin2Qty,self._bin3Qty,self._bin4Qty,self._bin5Qty,self._bin6Qty,self._bin7Qty,self._bin8Qty,self._inQty,self._yield = extractQty(data)
        if 'TOTAL TT' in data: # total TT
            self._totalTT = extract2ndColdata(data)
        if 'TOUCH DOWNS' in data: # Touch downs
            self._touchdownCnt = extract2ndColdata(data)

    ###############################################################################
    # check the platform according to the filename
    def checkPlatform(self, filename=None):
        if filename is not None:
            self._filename = filename # also for user to use
        parsedList = self.parseFilename(self._filename)
        if parsedList[0].lower() == 'shracku': # should not use 'is', 'is' is used for judge if 2 objects are totally same from memory level if they are using same memory
            self._testerPlatform = 'shracku'
        else:
            self._testerPlatform = 'adv'
    # open the file and yield the data line for external function handling
    def openFile(self, filename):
        #self._filename = os.path.basename(filename)
        self.checkPlatform()
        try:
            with open(filename,'r') as fi:
                for line in fi:
                    yield line
            for k in self._touchdown.keys():
                self._touchdown[k] = 0 
        except Exception as err:
            print('Error in openFile function: %s' % str(err))

    # intergrated handle full YE summary data
    def handleData(self, filename, summary=True, testblock=True, binning=True, tblist=None):
        self._filename = os.path.basename(filename)
        self.checkPlatform()
        for dataline in self.openFile(filename):
            if self._dataIsSummary(dataline):
                if summary:
                    self._collectSummaryData(dataline)
            elif 'end of summary' in dataline.lower(): # end of summary, yield summary info of this file
                if summary:
                    if self._isMT:
                        yield self._returnMTData()
                    else:
                        yield self._returnSTData()
            else:
                if testblock:
                    self._collectTestBlockData(dataline)

                    if 'tbtesttime:' in dataline.lower(): # get test block test time
                        yield self._returnTBTT()
                    elif 'activeduts_after' in dataline.lower(): # end of tb, yield duts info of this tb
                        if self._tbDataTracking:
                            for self._dut,self._dutData in self._tbDataTracking.items():
                                yield self._returnTBData()
                    elif 'bin:dut' in dataline.lower(): # containing binning info, yield
                        yield self._returnBinningData()

    #############################################################################


# ---------------------------------------------------------------------------------
# MT summary sample
"""
     START        = 2017/01/23 23:53:05            END          = 2017/01/23 23:57:18           
     CUSTOMER     = SANDISK                        DEVICE#      = 54-62-26247-128G              
     SANDISK LOT# = Q1701MEDB0.03                  WAFER LOT#   = WaferLot                      
     OPN          = SH             1ST_PASS        OPER#        = 27681                         
     PGM          = 40-47-TAC3037SH04_00           TOUCH DOWNS  = 1                             
     TESTER#      = ADTSP42                        TEMP         = 85                            
     HI-FIX       = 8b137076                       TOTAL TT     = 258.268 
"""
# --------------------------------------------------------------------------------
# ST summary sample
"""
 START        = 2017/12/01 00:45:01            END          = 2017/12/01 01:18:23           
 CUSTOMER     = SANDISK                        DEVICE#      = SDINBDD4-64-1209              
 SANDISK LOT# = M1747TA5A8.01                  WAFER LOT#   = WaferLot                      
 OPN          = SG             RESCREEN        OPER#        = EAP                           
 PGM          = tosp5af00_17                   TOUCH DOWNS  = 1                             
 TESTER#      = ADTSP28                        TEMP         = 25                            
 HI-FIX       = 4a138357                       TOTAL TT     = 2007.799                      
 FW           = IO4o4bC1055001601M10002C1986.bot DIECOUNT     = 2                             
 FWUPGRADE    =                                PGMREVISION  = 00_17                         
 Revision     = 20170316                       AverageTT    = 2007.80
 FORMATLBA    = 122142720                      KEYFILE    = OSQL1055Full_V01.der          
 RSAFILE      = OSQL1055Full_V01.sig           PRMFILE    = Osprey_eMMC_5_1_param_file_I001U015_BICS_EX3.txt
 EFFILE       = EFUSEPRODUCTIONFILE-OS-V02.TXT MEMTYPE    = P3262KESB2B3                  
 ASICID       = 8000                           MAXLBA     = 122191872                     
 CNE FW       = C7B56X12ACBIOP_Rev19.bot      
 HANDLER#     = ADH136                        

"""
# -----------------------------------------------------------------------------------

"""
YEPath = r'C:\Users\22222\Python\Database'
fileList = os.listdir(YEPath)
yeParser = YESummaryParser()
with open('output.txt','w') as fo:
    for filename in fileList:
        if filename.endswith('.1st') or filename.endswith('.rescreen'):
            for result in yeParser.handleData(os.path.join(YEPath,filename)):
                fo.write(','.join(result))
                fo.write('\n')

yeParser = YESummaryParser()
with open('output.txt','w') as fo:
    for filename in yeParser.searchYEFiles(regex='tosp5af00_18'):
        print('File: %s' % filename)
        for result in yeParser.handleData(os.path.join(os.getcwd(),filename)):
            fo.write(','.join(result))
            fo.write('\n')
 """       
