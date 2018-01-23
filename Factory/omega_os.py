import os
import glob
import shutil

class SearchAndCopy:
    # by default, kw is read from local file 'fileKeyWords.txt' and copy the result files to the localpath\search_result
    def __init__(self, searchFilePath, kwFile = r'C:\Users\22222\Python\TOOLS\FilesCopy\fileKeyWords.txt', copyFilePath=r'C:\Users\22222\Python\TOOLS\FilesCopy\search_result'):
        self._localSearchPath = searchFilePath
        self._currentCMDPath = os.getcwd()
        self._copyFilePath = os.path.join(self._currentCMDPath,copyFilePath)
        self._initPathCheck()
        self._wordsList = []
        self._kwFile = kwFile
        self._readKWFromFile()
        self._searchedFilesSet = set()
        
    
    def _startSearch(self):
        fileForFinding = ''
        filesFoundList = []
        self._searchedFilesSet.clear()
        for word in self._wordsList:
            #print(word)
            if word is not '':
                fileForFinding = self._localSearchPath+"\\*"+word+"*"
                filesFoundList = glob.glob(fileForFinding) # return a list which match the finding
                #print(filesFound)
            for fileFound in filesFoundList:
                self._searchedFilesSet.add(fileFound)
        #print(self._searchedFilesSet)

    def _startCopy(self):
        for fileFound in self._searchedFilesSet:
            OldPath, fileOldName = os.path.split(fileFound)
            NewPath, fileNewName = self._copyFilePath, fileOldName
            if os.path.exists(NewPath):
                newFilePath = os.path.join(NewPath, fileNewName)
                #print(newFilePath)
                shutil.copyfile(fileFound,newFilePath)
            else:
                raise "Error: %s doesn't exist" % NewPath
        
    def _initPathCheck(self):
        # check if search path is existed
        if not os.path.exists(self._localSearchPath):
            raise "Error: " + self._localSearchPath+" doesn't exist!"
        # remove the copy path and file first and make an empty folder
        if os.path.exists(self._copyFilePath):
            shutil.rmtree(self._copyFilePath)
        os.mkdir(self._copyFilePath)
        print("Searching path: %s" % self._localSearchPath)
        print("Result path: %s" % self._copyFilePath)

    def _readKWFromFile(self):
        # by default is using '\n' to split
        self._wordsList = []
        windows_command = 'start '+self._kwFile
        os.system(windows_command)
        choice = 'n'
        while choice.lower() != 'y':
            # raw_input will read data from command line directly
            # input will read python expression
            # e.g, you want to input a y or N
            # if using raw_input, you just need to input y in the command line
            # however, if using input, you have to input 'y' in the command line
            choice = raw_input('Search File Done? [y/N]')
            print(choice.lower())
          
        try:
            with open(self._kwFile,'r') as f:
                datas = f.read()
                for data in datas.split('\n'):
                    if data is not '' or data is not ' ':
                        self._wordsList.append(data)
        except Exception as err:
            print(str(err))
                    
    def updateKeyWords(self, kwList=[], resume=False):
        # resume - by default, kwList will replace the old key words list. combine old and new key words if set it true
        if resume:
            self._wordsList = self._wordsList + kwList
        else:
            self._wordsList = kwList
        
    def start(self):
        self._startSearch()
        self._startCopy()

    def listSearchedFiles(self):
        self._startSearch()
        return list(self._searchedFilesSet)

    def openResult(self):
        windows_command = 'start '+self._copyFilePath
        os.system(windows_command)

#searchFilePath = "C:\\Users\\22222\\Desktop\\YE"
searchFilePath = os.getcwd()
Search = SearchAndCopy(searchFilePath)

Search.start()
Search.openResult()


