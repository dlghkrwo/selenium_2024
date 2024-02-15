from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

url = 'https://www.naver.com'

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--headless=new")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get(url)



 