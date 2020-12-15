from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert 
from selenium import webdriver
import utils as tool
import chromedriver_autoinstaller
import json
import time
import os
import sys
import requests
import cassandraSent as bd


pathToHere=os.getcwd()

options = webdriver.ChromeOptions()

download_dir='C:\\Users\\1098350515\\Downloads'
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
               "download.default_directory": download_dir , 
               "download.prompt_for_download": False,
               "download.directory_upgrade": True,
               "download.extensions_to_open": "applications/pdf",
               "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
               }
options.add_experimental_option("prefs", profile)
#Erase every file in download folder at the beginning to avoid mixed files
for file in os.listdir(download_dir):
    os.remove(download_dir+'\\'+file)

print('Download folder empty...')
chromedriver_autoinstaller.install()
browser=webdriver.Chrome(options=options)
browser.get('chrome://settings/clearBrowserData')
browser.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER)
print('Browser data clear...')
#Since here both versions (heroku and desktop) are THE SAME
url="https://sise.cjf.gob.mx/consultasvp/default.aspx"
response= requests.get(url)
status= response.status_code
if status==200:  
    browser.get(url)
    try:
        WebDriverWait(browser, 5).until (EC.alert_is_present())
        #switch_to.alert for switching to alert and accept
        alert = browser.switch_to.alert
        alert.dismiss()
        browser.refresh()
    except TimeoutException:
        print('No alert found!')
        
    time.sleep(3)  
    #Read the information of query and page
    lsInfo=[]
    #1.Topic, 2. Page
    lsInfo=bd.getPageAndTopic()
    topic=str(lsInfo[0])
    page=str(lsInfo[1])
    startPage=int(page)
    print('Cassandra info:',str(startPage),'with query:',str(topic))

    #class names for li: rtsLI rtsLast
    liBuscar=browser.find_elements_by_xpath("//li[contains(@class,'rtsLI rtsLast')]")[0].click()
    strSearch=topic
    txtBuscar= browser.find_elements_by_id('txtTema')[0].send_keys(strSearch)
    btnBuscaTema=tool.devuelveElemento('//*[@id="btnBuscarPorTema_input"]',browser)
    btnBuscaTema.click()
    #WAit X secs until query is loaded.
    time.sleep(20)
    if startPage<=10:
        #Mechanism no failure
        for i in range(1,startPage):
            NextSinglePage=tool.devuelveElemento("//*[@id='grdSentencias_ctl00']/tfoot/tr/td/table/tbody/tr/td/div[3]/input[1]",browser)
            NextSinglePage.click()  
            time.sleep(5) 
        #End of non failire mechanism

    if startPage>10 and startPage<=100:
        if startPage>90:
            ten=10
        else:    
            ten=str(startPage)
            ten=int(ten[0])+1
        for times in range(1,ten):
            if times==1:
                SectionNextPages=browser.find_elements_by_xpath("//*[@id='grdSentencias_ctl00']/tfoot/tr/td/table/tbody/tr/td/div[2]/a[11]")[0].click()
                time.sleep(5)
                btnBuscaTema=tool.devuelveElemento('//*[@id="btnBuscarPorTema_input"]',browser)
                btnBuscaTema.click()
                time.sleep(5)
            else:
                SectionNextPages=browser.find_elements_by_xpath("//*[@id='grdSentencias_ctl00']/tfoot/tr/td/table/tbody/tr/td/div[2]/a[12]")[0].click()
                time.sleep(5)
                btnBuscaTema=tool.devuelveElemento('//*[@id="btnBuscarPorTema_input"]',browser)
                btnBuscaTema.click()
                time.sleep(5)

    #Rest for 10 seconds just to slow down
    time.sleep(10)
    print('Start reading the page...')
    #Control the page
    #Page identention
    while (startPage<=100):
        for row in range(0,20):
            tool.processRow(browser,strSearch,row)   
        #Update the info in file
        infoPage=str(browser.find_element(By.XPATH,'//*[@id="grdSentencias_ctl00"]/tfoot/tr/td/table/tbody/tr/td/div[5]').text)
        data=infoPage.split(' ')
        currentPage=int(data[2])
        print('Page already done:...',str(currentPage))   
        print('------------------------END--------------------------------------------') 
        control_page=int(currentPage)+1
        startPage=control_page
        #Edit  control file
        bd.updatePage(control_page)
        #Change the page with next
        print('Changing page...')
        #Non failure method: Seems that if first click is searach button it all refreshes
        btnBuscaTema=tool.devuelveElemento('//*[@id="btnBuscarPorTema_input"]',browser)
        btnBuscaTema.click()
        time.sleep(3)
        NextSinglePage=tool.devuelveElemento("//*[@id='grdSentencias_ctl00']/tfoot/tr/td/table/tbody/tr/td/div[3]/input[1]",browser)
        NextSinglePage.click()
        #End non ailure method
        time.sleep(5) 

    if startPage>100:
        print('Done with query: ',topic, ' . Please change topic')  
        os.sys.exit(0)  


browser.quit()
                           