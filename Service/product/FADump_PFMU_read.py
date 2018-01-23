from __future__ import print_function
import myExcel_1_0
import sys, os



class PFMU_Translater():
    def __init__(self):
        self._pfmu = None
    def translate(self, pfmu):
        self._pfmu = pfmu[pfmu.find('x')+1:]
        dec_PFMU = int(self._pfmu,16)
        print('extracted PFMU %s'% hex(dec_PFMU))
        dec_block = dec_PFMU//(2**16)
        dec_pln = ( ( dec_PFMU//(2**12) ) % 16 )/4
        blk_type = ( dec_PFMU//(2**12) ) % 4
        dec_FMUinBlk = dec_PFMU % (2**12)
        dec_wl, dec_str = 0, 0
        if blk_type == 0: # SLC
            dec_wl = dec_FMUinBlk//16
            dec_str = ( dec_FMUinBlk % 16 ) // 12
        else: # MLC
            dec_wl = dec_FMUinBlk//48
            dec_str = ( dec_FMUinBlk % 48 ) // 12
        dec_Die = dec_PFMU//(2**28)
        dec_LLT_address = (dec_block - dec_Die * 4096) * 2 + dec_pln
        print(','.join(['Failed PFMU:'+str(self._pfmu),'blk:'+hex(dec_block),'pln'+hex(dec_pln),'type:'+hex(blk_type),'fmu:'+hex(dec_FMUinBlk),'wl(d):'+str(dec_wl),'str:'+hex(dec_str),'llt:'+hex(dec_LLT_address),'die:'+hex(dec_Die)]))
        return ','.join(['Failed PFMU:'+str(self._pfmu),'blk:'+hex(dec_block),'pln'+hex(dec_pln),'type:'+hex(blk_type),'fmu:'+hex(dec_FMUinBlk),'wl(d):'+str(dec_wl),'str:'+hex(dec_str),'llt:'+hex(dec_LLT_address),'die:'+hex(dec_Die)])



class FADump_PFMU(myExcel_1_0.myExcel):
    def _translatePFMU(self, data):
        index = 0
        if data.find("\r") != -1:
            index = data.find("\r")
        elif data.find("\n") != -1:
            index = data.find("\n")
        print(data)
        failedPFMU = ''
        if index != 0:
            failedPFMU = data[data.find("x")+1:index]
        else:
            failedPFMU = data[data.find("x")+1:]
        #print('original PFMU: %s' % failedPFMU)
        dec_PFMU = int(failedPFMU,16)
        print('extracted PFMU %s'% hex(dec_PFMU))
        dec_block = dec_PFMU//(2**16)
        #print('blk: '+hex(dec_block))
        dec_pln = ( ( dec_PFMU//(2**12) ) % 16 )/4
        #print('pln: '+hex(dec_pln))
        blk_type = ( dec_PFMU//(2**12) ) % 4
        #print('type: '+hex(blk_type))
        dec_FMUinBlk = dec_PFMU % (2**12)
        #print('FMU in Blk: '+hex(dec_FMUinBlk))
        dec_wl, dec_str = 0, 0
        if blk_type == 0: # SLC
            dec_wl = dec_FMUinBlk//16
            dec_str = ( dec_FMUinBlk % 16 ) // 12
        else: # MLC
            dec_wl = dec_FMUinBlk//48
            dec_str = ( dec_FMUinBlk % 48 ) // 12
        dec_Die = dec_PFMU//(2**28)
        dec_LLT_address = (dec_block - dec_Die * 4096) * 2 + dec_pln
        print(','.join(['blk:'+hex(dec_block),'pln'+hex(dec_pln),'type:'+hex(blk_type),'fmu:'+hex(dec_FMUinBlk),'wl(d):'+str(dec_wl),'str:'+hex(dec_str),'llt:'+hex(dec_LLT_address),'die:'+hex(dec_Die)]))
        return ','.join(['Failed PFMU:'+str(failedPFMU),'blk:'+hex(dec_block),'pln'+hex(dec_pln),'type:'+hex(blk_type),'fmu:'+hex(dec_FMUinBlk),'wl(d):'+str(dec_wl),'str:'+hex(dec_str),'llt:'+hex(dec_LLT_address),'die:'+hex(dec_Die)])
        
    
    def handleWithData(self, rowdata, fh):
        for data in rowdata:
            if 'BMX:' in data:
                fh.write(data+',')
            if 'PFMU:' in data:
                fh.write(self._translatePFMU(data))
outputfile = 'oooo.txt'
argument = sys.argv[1]
if argument.endswith('xlsx') or argument.endswith('xls'):
    filename = argument
    print(filename)
    FADump_workbook = FADump_PFMU(filename)
    with open(outputfile, mode='w') as fo:   
        for rowdata in FADump_workbook.yieldRowWithSpecialContent('PFMU:'):
            FADump_workbook.handleWithData(rowdata,fo)
            fo.write('\n')
    os.system('start '+outputfile)
else:
    pfmu_translater = PFMU_Translater()
    pfmu_translater.translate(argument)
