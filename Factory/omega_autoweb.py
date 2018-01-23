from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

class omega_autoweb():
        
    def __init__(self):
        self._browser = webdriver.Chrome() # default browser is using Chrome
        self._defaultTimeout = 10 # default timeout for page/element loading is 10s

    # check and return the first element if it is loaded successfully
    def _getElement(self, selectType, selector):
        try:
            if selectType == 'xpath':
                return WebDriverWait(self._browser,self._defaultTimeout).until(lambda x: x.find_element_by_xpath(selector))
            elif selectType == 'css':
                return WebDriverWait(self._browser,self._defaultTimeout).until(lambda x: x.find_element_by_css_selector(selector))
            elif selectType == 'id':
                return WebDriverWait(self._browser,self._defaultTimeout).until(lambda x: x.find_element_by_id(selector))
            elif selectType == 'text':
                return WebDriverWait(self._browser,self._defaultTimeout).until(lambda x: x.find_element_by_link_text(selector))
            elif selectType == 'name':
                return WebDriverWait(self._browser,self._defaultTimeout).until(lambda x: x.find_element_by_name(selector))
            else:
                print('selector: %s not found! Only support: xpath, css, id, text, name' % selector)
        except Exception as err:
            self._exceptionHandle(str(err))

    # check and return all elements
    def _getElements(self, selectType, selector):
        try:
            if selectType == 'xpath':
                return WebDriverWait(self._browser,self._defaultTimeout).until(lambda x: x.find_elements_by_xpath(selector))
            elif selectType == 'css':
                return WebDriverWait(self._browser,self._defaultTimeout).until(lambda x: x.find_elements_by_css_selector(selector))
            elif selectType == 'id':
                return WebDriverWait(self._browser,self._defaultTimeout).until(lambda x: x.find_elements_by_id(selector))
            elif selectType == 'text':
                return WebDriverWait(self._browser,self._defaultTimeout).until(lambda x: x.find_elements_by_link_text(selector))
            elif selectType == 'name':
                return WebDriverWait(self._browser,self._defaultTimeout).until(lambda x: x.find_elements_by_name(selector))
            else:
                print('selector: %s not found! Only support: xpath, css, id, text, name' % selector)
        except Exception as err:
            self._exceptionHandle(str(err))

    def _exceptionHandle(self, message):
        print(message)
        self.shutDown()
    """
    Robot Action
    """
    # close the browser window
    def closeWindow(self):
        self._browser.close()

    # shut down the connection
    def shutDown(self):
        self._browser.quit()

    # load the page
    def loadPage(self, url):
        try:
            self._currentURL = url
            self._browser.get(self._currentURL)
        except Exception as err:
            self._exceptionHandle(('URL: %s can\'t be accessed! < %s >' % (url,str(err))))

    def getPageSource(self):
        return self._browser.page_source

    def getElemsFromPageSrc(self, css_selector):
        pass
        
    def setDefaultTimeout(self, newTimeout):
        self._defaultTimeout = newTimeout

    # send keys to input
    def inputSendKeys(self, selectType, selector, content):
        try: 
            InputWidget = self._getElement(selectType, selector)
            if InputWidget is not None:
                InputWidget.clear()
                InputWidget.send_keys(content)
        except Exception as err:
            self._exceptionHandle(str(err))

    # click button
    def buttonClick(self, selectType, selector):
        try:
            buttonWidget = self._getElement(selectType, selector)
            if buttonWidget is not None:
                buttonWidget.click()
        except Exception as err:
            self._exceptionHandle(str(err))

    # send keys to input and click button
    def inputAndClick(self, inputSelectType=None, inputSelector=None, content=None, buttonSelectType=None, buttonSelector=None):
        if [inputSelectType, inputSelector,content,buttonSelectType,buttonSelector] is not [None,None,None,None,None]:
            self.inputSendKeys(inputSelectType, inputSelector, content)
            self.buttonClick(buttonSelectType, buttonSelector)
        else:
            self._exceptionHandle('wrong argument')

    # get the text infomation
    def getText(self, selectType, selector):
        return self._getElement(selectType, selector).text
    
    def getFirstElement(self, selectType, selector):
        return self._getElement(selectType, selector)
        
    def getAllElements(self, selectType, selector):
        return self._getElements(selectType, selector)
    
    def switchFrame(self, frameID):
        self._browser.switch_to.frame(frameID)
        
    def switchBack(self):
        self._browser.switch_to.parent_frame()

