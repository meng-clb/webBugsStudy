import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 实例化谷歌浏览器驱动
chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
web = Chrome(options=chrome_options)

web.get('https://www.gushiwen.cn/')
# 获取搜索框
txtKey = web.find_element(By.ID, 'txtKey')
# 向搜索框内输入内容
txtKey.send_keys('李白')
search = web.find_element(By.XPATH, '//*[@id="search"]/form/input[3]')
search.click()

time.sleep(100)
# time.sleep(1000)
