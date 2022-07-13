from selenium import webdriver
from time import sleep
#无头浏览器
from selenium.webdriver.chrome.options import Options
#规避检测
from selenium.webdriver import ChromeOptions

Chrome_options = Options()
Chrome_options.add_argument('--headless')
Chrome_options.add_argument('--disable--gpu')
#规避检测：
option=ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])
driver=Chrome(options=option)


driver = webdriver.Chrome(options=Chrome_options)
driver.get('https://www.baidu.com/')

