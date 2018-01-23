
# SLICE NAME
FOUNDRY = slice(0,1)
WAFER_SIZE = slice(1,2)
WAFER_Mb = slice(2,6)
WAFER_TECH_1 = slice(6,7)
WAFER_TECH_2 = slice(7,8)
WAFER_DENSITY = slice(8,10)
BLOCK_SIZE = slice(10,11)
VOLTAGE = slice(11,12)

# SLOT DETAIL
FOUNDRY_SLOT = {
    'A':'Flash Aliance',
    'B':'Billionton',
    'C':'Micron Semiconductor Products, Inc',
    'D':'Intel',
    'F':'Fujitsu',
    'H':'Hynix',
    'I':'Fujifilm',
    'K':'Toshiba Non-Partner',
    'M':'Sony',
    'N':'Flash Vision/Toshiba',
    'O':'Olympus',
    'P':'SNDK-TSB Parter',
    'R':'Renesas',
    'S':'Samsung',
    'T':'TSMC',
    'U':'UMC',
    'X':'Unknown',
    }
WAFER_SIZE_SLOT ={
    '2':'200mm',
    '3':'300mm',
    'X':'Unknown',
    }
WAFER_Mb_SLOT = {
    '01M4':'1.36Tb -> 1360Gb',
    '001M':'1048576Mb -> 1024Gb',
    '524K':'524288Mb -> 512Gb',
    '262K':'262144Mb -> 256Gb',
    '204K':'204800Mb -> 200Gb',
    '131K':'131072Mb -> 128Gb',
    '098K':'98304Mb -> 96Gb',
    '102K':'102400Mb -> 100Gb',
    '065K':'65536Mb -> 64Gb',
    '032K':'32768Mb -> 32Gb',
    '016K':'16384Mb -> 16Gb',
    '8192':'8192Mb -> 8Gb',
    '4096':'4096Mb -> 4Gb',
    '2048':'2048Mb -> 2Gb',
    '1024':'1024Mb -> 1Gb',
    '128':'1280Mb',
    '512':'512Mb',
    '256':'256Mb',
    'X':'Unknown',
    }
WAFER_TECH_1_SLOT = {
    'B':'Binary/SLC',
    'M':'Multi Level Cell (MLC)',
    'E':'Multi Level Cell (MLC) Enhanced Non VLV',
    'H':'Multi Level Cell (MLC) Enhanced High Endurance',
    'N':'Multi Level Cell (MLC) Enhanced SECC / LDPC',
    'R':'Multi Level Cell (MLC) Enhanced Cost reduction Die',
    'S':'Multi Level Cell (MLC) SECC',
    'V':'Multi Level Cell (MLC) Enhanced VLV',
    'X':'Unknown, and or not Applicable',
    }
WAFER_TECH_2_SLOT = {
    'A':'All Bit Line (ABL)  X2',
    'C':'Conventional',
    'D':'All Bit Line (ABL) X3',
    'E':'All Bit Line (ABL) X4',
    'H':'Half Bit Line (HBL)',
    'J':'All Bit Line (ABL) X2 2 Plane',
    'K':'All Bit Line (ABL) X2 4 Plane',
    'M':'All Bit Line (ABL) X4 2 Plane',
    'S':'All Bit Line (ABL) X3 2 Plane',
    '0':'CMOS only',
    '2':'2 Layer',
    '4':'4 Layer',
    'X':'Unknown',
    }
WAFER_DENSITY_SLOT = {
    'B4':'BiCs 4th generation',
    'B3':'BiCs 3rd generation',
    'B2':'BiCs 2nd generation',
    'B1':'BiCs 1st generation',
    '1A':'1A',
    '1Z':'1Z',
    '1Y':'1Y',
    '1X':'1X',
    '16':'16nm',
    '20':'20nm',
    '24':'24nm',
    '25':'25nm',
    '34':'34nm',
    '32':'32nm',
    '43':'43nm',
    '52':'52nm',
    '55':'55nm',
    '56':'56nm',
    '70':'70nm',
    '80':'80nm',
    '90':'90nm',
    '12':'120nm',
    '13':'130nm',
    '15':'150nm',
    '16':'160nm',
    'XX':'Unknown',
    }
BLOCK_SIZE_SLOT = {
    'B':'Big Block, Standard die, bucket1',
    'F':'Cherry Pick Fallout',
    'L':'Special code for planning system',
    'R':'Planning code for Relax DS / RTL',
    'S':'Small Block',
    'X':'Unknown',
    }
VOLTAGE_SLOT = {
    '1':'1.8 Volts',
    '3':'3.0 Volts',
    'v':'Dual Voltage',
    'X':'Unknown',
    }

class memtypeParser:

    def __init__(self, *args):
        self._memtype = [m for m in args]
        self._defaultLen = 12


    def _parseMemType(self,memtype=None):
        memtype = memtype.upper()
        return [
            self._dataFormat(memtype[FOUNDRY],FOUNDRY_SLOT[memtype[FOUNDRY]]),
            self._dataFormat(memtype[WAFER_SIZE],WAFER_SIZE_SLOT[memtype[WAFER_SIZE]]),
            self._dataFormat(memtype[WAFER_Mb],WAFER_Mb_SLOT[memtype[WAFER_Mb]]),
            self._dataFormat(memtype[WAFER_TECH_1],WAFER_TECH_1_SLOT[memtype[WAFER_TECH_1]]),
            self._dataFormat(memtype[WAFER_TECH_2],WAFER_TECH_2_SLOT[memtype[WAFER_TECH_2]]),
            self._dataFormat(memtype[WAFER_DENSITY],WAFER_DENSITY_SLOT[memtype[WAFER_DENSITY]]),
            self._dataFormat(memtype[BLOCK_SIZE],BLOCK_SIZE_SLOT[memtype[BLOCK_SIZE]]),
            self._dataFormat(memtype[VOLTAGE],VOLTAGE_SLOT[memtype[VOLTAGE]]),
            ]

    def _isValidMemType(self, memtype=None):
        if len(memtype) == 12:
            return True
        else:
            return False
    def _yieldMemType(self):
        for memtype in self._memtype:
            yield memtype

    def _dataFormat(self, src, description):
        return '%s => %s' % (src,description)
    
    def parse(self):
        for memtype in self._yieldMemType():
            if self._isValidMemType(memtype):
                for result in self._parseMemType(memtype):
                    yield result
            else:
                print('MemType: %s is not valid!\n' % memtype)
        
