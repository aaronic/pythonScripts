import csv
import os
import sys

class csvReader():
    def __init__(self, csvObj=None):
        self._reader = csv.reader(csvObj)

    def next(self):
        row = self._reader.next()
        return row
    def __iter__(self):
        return self    

class csvWriter():
    def __init__(self, fileObj=None, dialect=csv.excel):
        self._writer = csv.writer(fileObj,dialect=dialect)
    def writerow(self,row):
        self._writer.writerow(row)
        
class omega_csv(object):
    def __init__(self, f=None):
        self._file = f
        self._datasline = None

    def read(self):
        with open(self._file,'rb') as f:
            for self._datasline in csvReader(f):
                yield self._datasline
    
    def handleData(self,data):
        pass

"""
op = csvOperator('uid_data.csv')
for (op.read()):
    op.handleData()
"""
"""
with open('uid_data.csv','rb') as f:
    for data in csvReader(f):
        print(data)
"""
