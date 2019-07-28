from selenium import webdriver
from pyquery import PyQuery as pq
import re
import time

browser = webdriver.Chrome()

browser.get('http://www.bjsubway.com/e/action/ListInfo/?classid=39&ph=1')

# 获取网页源码
html_source = browser.page_source
doc = pq(str(html_source))
lines = []

# 地铁路线字典，k=line，v=stations
subway_dict = {}
for i in range(20):
    line_id = '#sub' + str(i) + ' .con_text table thead tr:first-child'
    station_id = '#sub' + str(i) + ' .con_text table tbody'
    line_text = doc(line_id).text().split(' ')
    table_body = doc(station_id)
    for j in range(len(table_body)):
        line = line_text[j].replace('首末车时刻表', '')
        if line in lines: continue
        lines.append(line)
        stations_data = re.findall('[\u4e00-\u9fa5]+', doc(table_body[j]).text())
        while '暂缓开通' in stations_data:
            stations_data.remove('暂缓开通')
        _stations = stations_data[::2] if line == '4号线/大兴线' else stations_data
        print(line, _stations)
        stations = sorted(set(_stations), key=_stations.index)
        subway_dict[line] = stations

# 搜索每个站点的位置
browser.get('https://lbs.amap.com/console/show/picker')
with open('subway0.txt', 'w') as f:
    f.write('line,station,dimension,longitude\n')
    for line, stations in subway_dict.items():
        for station in stations:
            if len(station) > 7: continue
            browser.find_element_by_id('txtSearch').clear()
            time.sleep(0.2)
            if station == '通州北苑':
                browser.find_element_by_id('txtSearch').send_keys(station)
            else:
                browser.find_element_by_id('txtSearch').send_keys(station + '地铁站')
            browser.find_element_by_class_name('btn-search').click()
            position = browser.find_element_by_id('txtCoordinate').get_attribute('value')
            per_line = line + ',' + station + ',' + position + '\n'
            print(per_line)
            f.write(per_line)

print('over over')
