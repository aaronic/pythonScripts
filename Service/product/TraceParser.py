import sys
import re
sys.path.append(r'C:\Users\22222\pythonScripts\Factory')
from omega_csv import *


       
# INDEX
ROW_ID = 0
TIMESTAMP = 1
TYPE = 2
ID = 3
NAME = 4
PARAM = 5
BOUND = 6
SOURCE = 7
TASK_ID = 8
DURATION = 9
MATE_ROW = 10
TIME_VIOLATION = 11

# SPECIAL CASE
NAND_SOURCE = '4' # source = 4 is Memory command

class TraceParser(omega_csv):
    def __init__(self,trace=None):
        super(TraceParser, self).__init__(trace)
        self._kw_chip = [
            'Chip 0 Single Chip Selection',
            'Chip 1 Single Chip Selection',
        ]
        #self._traceDescriptor = TraceDescriptor()

        self._title = {
            'Row_Id'        : 0,
            'Timestamp'     : 1,
            'Type'          : 2,
            'ID'            : 3,
            'Name'          : 4,
            'Parameters'    : 5,
            'Bound'         : 6,
            'Source'        : 7,
            'Task_ID'       : 8,
            'Duration'      : 9,
            'Mate_Row'      : 10,
            'Time_Violation': 11
        }
        self._chip = -1
        
    # check if the data source is from NAND
    def isSrc4(self,*datas):
        if datas:
            self._datasline = datas
        if self._datasline[SOURCE] == NAND_SOURCE:
            return True
        else:
            return False
    # collect die trace, by default, only collect source 4 of chip 0
    def collectDieTrace(self, chip=0, src=4, *datas):
        if datas:
            self._datasline = datas
        if self._datasline[SOURCE] == str(src):
            for index,value in enumerate(self._kw_chip):
                if self._datasline[NAME] == value:
                    self._chip = index
                    break
            if str(self._chip) == str(chip): # get the target chip
                return self._datasline
            else:
                return None
        else:
            return None

die = 0 # extract die 0 by default
src = 4 # extract src 4 by default
if len(sys.argv) > 1:
    die = sys.argv[1]
if len(sys.argv) > 2:
    src = sys.argv[2]
    
with open('parsedTrace.txt','w') as fo:
    for csvFile in [i for i in os.listdir(os.getcwd()) if i.endswith('.csv')]:
        tp = TraceParser(csvFile)
        for datasline in tp.read():
            result = tp.collectDieTrace(chip=die, src=src)
            if result:
                fo.write(','.join(result))
                fo.write('\n')


