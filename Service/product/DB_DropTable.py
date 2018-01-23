import sys
import os
sys.path.append(r'C:\Users\22222\pythonScripts\Factory')
from omega_db import *

dbList = None
if len(sys.argv) >= 2:
    dbList = sys.argv[1:]
else:
    dbList = [db for db in os.listdir(os.getcwd()) if db.endswith('.db')]

for dbName in dbList:
    print('DB: %s' % dbName)
    db = omega_db()
    db.connectDB(dbName)
    print(db.getAllTables())
    db.deleteTables(regex=r'(SA)|(SG)|(SS)|(Q6)_0x.*')
db.saveDB()
db.closeDB()
    
