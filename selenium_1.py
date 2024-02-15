from xml.dom.pulldom import END_ELEMENT
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

import time

customService = Service(ChromeDriverManager().install())
customOption = Options()
browser = webdriver.Chrome(service= customService, options= customOption)

url = "http://www.google.com"

browser.get(url)
browser.implicitly_wait(10)
# time.sleep(3)

# temp = browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/a').text
# print(temp)

# browser.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea').send_keys('hihihi')
# time.sleep(2)

# browser.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[3]/div[3]/svg').click()
# time.sleep(3)

#for loop to get all the elements
# for i in range(1, 101, 1):
#     find_ELEMENT(By.XPATH, f'//html/body/div[3]/main/div[2]/div[3]/div/div/div/div[2]/div[8]/ul/li[3]')

#if new window browers open -> window method() required
#if capcha while login -> existance of alternative way by the browser website
#used .text to crawling the data but not collected -> wait little bit by using time.sleep()


