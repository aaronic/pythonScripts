import xlrd
import xlwt

class myExcel():

    def __init__(self, filename=None, sheetName='Sheet1'):
        self.workbook = None
        self.sheet = None
        self._openExcel(filename)
        self._selectSheetbyName(sheetName)
    
    def _openExcel(self, filename=None):
        try:
            self.workbook = xlrd.open_workbook(filename,on_demand=True)
        except Exception as err:
            print(str(err))
    
    def _selectSheetbyName(self,sheetName='Sheet1'):
        try:
            self.sheet = self.workbook.sheet_by_name(sheetName)
        except Exception as err:
            print(str(err))
    
    def _getNumOfRowsAndCols(self):
        try:
            return [self.sheet.nrows,self.sheet.ncols]
        except Exception as err:
            print(str(err))
    
    def _getCellValue(self, rowIndex=0, colIndex=0):
        try:
            return self.sheet.cell(rowIndex, colIndex).value
        except Exception as err:
            print(str(err))
    
    def yieldRowWithSpecialContent(self,content=None):
        try: 
            numOfRows, numOfCols = self._getNumOfRowsAndCols()
            for row in range(numOfRows):
                for col in range(numOfCols):
                    cellValue = self._getCellValue(row, col)
                    if content in cellValue:
                        yield self.sheet.row_values(row)
                        break # go to next row
        except Exception as err:
            print(str(err))
    
    def handleWithRowData(rowData):
        pass
