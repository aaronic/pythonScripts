import sqlite3 as dbapi
import re


class sqlCmd():
    def __init__(self):
        self._table = None
        self._sqlcmd = None
    def cmd_ceateTable(self, tableName, colNameTypeString):
        self._sqlcmd = 'CREATE TABLE IF NOT EXISTS "'+ tableName+ '"(' + colNameTypeString + ')'
    # WHERE must be before the ORDER BY, becaues ORDER BY is to order the extracted data, WHERE is for extracting data
    def cmd_selectDataFromTable(self, tableName, selectColString, where, orderByCol, seq):
        self._sqlcmd = 'SELECT ' + selectColString + ' FROM ' + tableName
        if where is not None:
            self._sqlcmd += ' WHERE ' + where           
        if orderByCol is not None:
            self._sqlcmd += ' ORDER BY ' + orderByCol
        if seq is not None:
            self._sqlcmd += ' ' + seq
    def cmd_insertDataIntoTable(self, tableName, dataString):
        self._sqlcmd =  'INSERT INTO ' + tableName + ' VALUES(' + dataString + ')'
    def cmd_insertDataWithColname(self, tableName, colString, dataString):
        self._sqlcmd = 'INSERT INTO ' + tableName + '(' + colString + ') VALUES(' + dataString + ')'
        
    def cmd_updateData(self, tableName, colName, colData, rowName, rowData):
        self._sqlcmd = 'UPDATE ' + tableName + ' SET ' + colName + ' = "' + str(colData) + '" WHERE ' + rowName + ' = "' + str(rowData) + '"'
    def cmd_dropTable(self, tableName):
        self._sqlcmd = 'DROP TABLE ' + tableName
    def cmd_PRAGMA(self, tableName):
        self._sqlcmd = 'PRAGMA table_info(' + tableName + ')'
    def cmd_unionTables(self, tableName1, tableName2, selectColString):
        self._sqlcmd = 'SELECT ' + selectColString + ' FROM '+ tableName1 + ' UNION SELECT ' + selectColString + ' FROM ' + tableName2 
    def getAllTables(self):
        self._sqlcmd = 'SELECT name FROM sqlite_master WHERE type="table"'
    def getCmd(self):
        return self._sqlcmd


class omega_db():
    def __init__(self):
        self._connection = None
        self._cursor = None
        self._cmd = sqlCmd()
    # connect to DB
    def connectDB(self, dbPath):
        self._connection = dbapi.connect(dbPath)
        self._cursor = self._connection.cursor()
    # create table  
    def createTable(self, tableName, colNameTypeString):
        self._cmd.cmd_ceateTable(tableName, colNameTypeString)
        self._cursor.execute(self._cmd.getCmd())
    # select data, return all data
    def selectDataFromTable(self, tableName, selectColString, where = None, orderByCol=None, seq=None):
        self._whereConditionCheck(where)
        self._cmd.cmd_selectDataFromTable(tableName, selectColString, where, orderByCol, seq)
        self._cursor.execute(self._cmd.getCmd())
        return self._cursor.fetchall()
    # insert single data which hasn't specific col  
    def insertDataIntoTable(self, tableName, dataList):
        try:
            dataString = ','.join(self.adjustDataFormat(tableName,dataList))
            self._cmd.cmd_insertDataIntoTable(tableName, dataString)
            self._cursor.execute(self._cmd.getCmd())
        except Exception as err:
            #print('%s: %s' %(str(err), dataString))
            pass
    # insert data with col specified
    def insertDataWithColname(self, tableName, colString, dataList):
        modifiedDataList = []
        try:
            for index,colname in enumerate(colString.split(',')):
                modifiedDataList.append(self.adjustColDataFormat(tableName,colname,dataList[index]))
            modifiedDataString = ','.join(modifiedDataList)
            self._cmd.cmd_insertDataWithColname(tableName,colString,modifiedDataString)
            self._cursor.execute(self._cmd.getCmd())
        except Exception as err:
            print(str(err))
            #pass
    # insert data list
    def insertMultiData(self, tableName, dataStringList):
        for dataString in dataStringList:
            self.insertDataIntoTable(tableName, dataString)
    # update data
    def updateData(self, tableName, colName, colData, rowName, rowData):
        self._cmd.cmd_updateData(tableName, colName,colData, rowName, rowData)
        self._cursor.execute(self._cmd.getCmd())
    # execute SQL command directly and return the response
    def executeSQLCmd(self, cmd):
        self._cursor.execute(cmd)
        return self._cursor.fetchall()
    # delete table
    def deleteTable(self, tableName):
        self._cmd.cmd_dropTable(tableName)
        self._cursor.execute(self._cmd.getCmd())
    def deleteTables(self,regex=None, *tableNames):
        tbList = tableNames if tableNames else self.getAllTables()
        for tableName in tbList:
            print(tableName)
            if re.match(regex,tableName) is not None:
                print('delete %s' % tableName)
                self.deleteTable(tableName)                
    # save database
    def saveDB(self):
        self._connection.commit()
    # close the connection of DB
    def closeDB(self):
        self.saveDB()
        self._connection.close()
    # get all columns name and type
    def getAllColsNameAndType(self, tableName):
        self._cmd.cmd_PRAGMA(tableName)
        self._cursor.execute(self._cmd.getCmd())
        return self._cursor.fetchall()
    # adjust data format in the data list
    def adjustDataFormat(self, tableName, colDataList):
        modifiedDataList = []
        for index, colInfo in enumerate(self.getAllColsNameAndType(tableName)):
            #print('col: %s type: %s' %(colInfo[1],colInfo[2]))
            colType = colInfo[2]
            tmp_data = colDataList[index]
            #print('orig data: %s' % tmp_data)
            if 'TEXT' in colType:
                tmp_data = '"'+tmp_data+'"'
            #print('modified data: %s' % tmp_data)
            modifiedDataList.append(tmp_data)
        return modifiedDataList
    # check the specific column type
    def checkColDataType(self, tableName, colName):
        for colInfo in self.getAllColsNameAndType(tableName):
            name = colInfo[1]
            if colName == name:
                return colInfo[2]
    # modify the specific column data format
    def adjustColDataFormat(self, tableName, colName, colData):
        #print('check col:%s data: %s type' %(colName,colData))
        colType = self.checkColDataType(tableName, colName)
        #print('col: %s data: %s type: %s' %(colName,colData,colType))
        if 'TEXT' in colType:
            return '"'+str(colData)+'"'
        else:
            return str(colData)

    def _whereConditionCheck(self,where):
        pass
        #where = where.strip()
        #datalist = re.split('[=]+',where)
        
        
    # check if the key is already in DB
    def isNotInDB(self, tableName, primarykey, keyvalue):
        modifiedValue = self.adjustColDataFormat(tableName,primarykey,keyvalue)
        datalist = self.executeSQLCmd('SELECT * FROM ' + tableName + ' WHERE ' + primarykey + '=' + modifiedValue)
        if len(datalist) > 0: # has record
            return False
        else:
            return True
    # get table names in DB
    def getAllTables(self):
        """[(u'SA_1st_0x0000',), (u'SA_1st_0x99CE',)]
        """
        self._cmd.getAllTables()
        self._cursor.execute(self._cmd.getCmd())
        tableList = [tbName[0] for tbName in self._cursor.fetchall()]
        #return self.executeSQLCmd('SELECT name FROM sqlite_master WHERE type="table"')
        return tableList

    def unionTables(self, tableName1, tableName2, selectColString):
        self._cmd.cmd_unionTables(tableName1, tableName2,selectColString)
        self._cursor.execute(self._cmd.getCmd())
        return self._cursor.fetchall()

    def joinTablesCondition(self, tableFrom, tableJoin, selectColString, compareCol, where):
        modifiedList = []
        for colname in selectColString.split(','):
            modifiedList.append(tableFrom + '.' + colname)
        tmpstring = ','.join(modifiedList)
        cmd = 'SELECT '+tmpstring+' FROM '+tableFrom+' JOIN '+tableJoin+' ON '+'='.join(['.'.join([tableFrom,compareCol]),'.'.join([tableJoin,compareCol])])+' WHERE '+where
        return self.executeSQLCmd(cmd)
