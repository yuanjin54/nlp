from selenium import webdriver
from pyquery import PyQuery
import time

browser = webdriver.Chrome()
browser.get('https://lbs.amap.com/console/show/picker')

stations = ['宋家庄', '经海路', '次渠南']

while stations:
    browser.find_element_by_id('txtSearch').clear()
    time.sleep(1)
    browser.find_element_by_id('txtSearch').send_keys(stations.pop(0))
    browser.find_element_by_class_name('btn-search').click()
    ans = browser.find_element_by_id('txtCoordinate').get_attribute('value')
    print(ans)

# html = browser.page_source
# data = str(html)
# print(data)