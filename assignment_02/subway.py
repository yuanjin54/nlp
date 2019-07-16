from selenium import webdriver
import time

browser = webdriver.Chrome()
# html = browser.page_source
# data = str(html)
browser.get('https://www.bjsubway.com/station/xltcx/')

subway_text = browser.find_element_by_class_name('line_content').text

subway_list = str(subway_text).split('\n')

lines = ['1号线', '2号线', '4号线', '5号线', '6号线', '7号线', '8号线北', '8号线南', '9号线', '10号线', '13号线', '14号线西', '14号线东', '15号线',
         '16号线', '八通线', '昌平线', '亦庄线', '房山线', '机场线', 'S1线', '燕房线', '西郊线']

line = ''

browser.get('https://lbs.amap.com/console/show/picker')

with open('subway.txt', 'w') as file:
    file.write('line,station,dimension,longitude\n')
    for ele in subway_list:
        if len(ele) > 7: continue
        if ele in lines:
            line = ele
            continue
        browser.find_element_by_id('txtSearch').clear()
        time.sleep(0.4)
        browser.find_element_by_id('txtSearch').send_keys(ele + '地铁站')
        browser.find_element_by_class_name('btn-search').click()
        position = browser.find_element_by_id('txtCoordinate').get_attribute('value')
        file.write(line + ',' + ele + ',' + position + '\n')

print('The end')
