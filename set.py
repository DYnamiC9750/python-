from mainS0 import *

# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')

# # 实现规避检测
# options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome()
driver.maximize_window()


load('15888269750', 'Sakura7777', driver)
# findClass()
className = ('创业基础-第2版')
findClass(driver, className)
findVideo(driver)
playVideo(driver)
# Next_chapter(driver)

driver.quit()
