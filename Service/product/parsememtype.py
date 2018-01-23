import sys
sys.path.append(r'C:\Users\22222\pythonScripts\Factory')
from omega_memtype import *


if len(sys.argv) >= 2:
    for memtype in sys.argv[1:]:
        print('Memtype: %s' % memtype)
        for result in memtypeParser(memtype).parse():
            print(result)
else:
    print('Please take at least 1 argument\n')
        
