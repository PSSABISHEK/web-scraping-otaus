from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import os
import time

chromedriver = "C:\\Users\\asus\\Downloads\\chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
url='https://www.otaus.com.au/find-an-ot'
driver.get(url)
driver.maximize_window()
select = Select(driver.find_element_by_name('ServiceType'))
select.select_by_value('1')
driver.find_element_by_class_name('submit').submit()
time.sleep(8)
ctrData = 1
ctrPages = 4
constPage = 10
OTData = []
for j in range(50):
    data = driver.find_elements_by_class_name('main-contact-content')
    for i in data:
        local=[]
        title = i.find_element_by_xpath('//*[@id="main-result-list"]/div[{0}]/div[2]/div[1]/div[1]/div'.format(str(ctrData))).text
        local.append(title)
        name = i.find_element_by_xpath('//*[@id="main-result-list"]/div[{0}]/div[2]/div[1]/div[1]/p[1]/strong'.format(str(ctrData))).text
        local.append(name)
        address = i.find_element_by_xpath('//*[@id="main-result-list"]/div[{0}]/div[2]/div[1]/div[1]/p[2]'.format(str(ctrData))).text
        address.replace('\n', '')
        local.append(address)
        try:
            mobile = i.find_element_by_xpath('//*[@id="main-result-list"]/div[{0}]/div[2]/div[1]/div[1]/p[4]/a'.format(str(ctrData))).text
            local.append(mobile)
        except:
            local.append('')
            pass
        try:
            email = i.find_element_by_xpath('//*[@id="main-result-list"]/div[{0}]/div[2]/div[1]/div[1]/p[7]/a'.format(str(ctrData))).text
            local.append(email)
        except:
            local.append('')
            pass
        ctrData += 1
        OTData.append(local)
    if(ctrPages==14):
        bttn = data[0].find_element_by_xpath('//*[@id="search-result"]/div[4]/ul/li[{0}]/a'.format(str(constPage)))
        driver.execute_script("arguments[0].click();", bttn)
    else:
        bttn = data[0].find_element_by_xpath('//*[@id="search-result"]/div[4]/ul/li[{0}]/a'.format(str(ctrPages)))
        driver.execute_script("arguments[0].click();", bttn)
        ctrPages += 1
    time.sleep(8)
    ctrData = 1
    print('Done')
df = pd.DataFrame(OTData, columns=['title', 'name', 'address', 'mobile', 'email'])
df.to_csv('list.csv', index=False)