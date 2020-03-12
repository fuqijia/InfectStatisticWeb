import requests
import json
import re
import time
from ppp import models


def insert_item(item, type_):
    '''
    插入数据到mongodb，item为要插入的数据，type_用来选择collection
    '''

    if type_ == 'dxy_map':
        # 更新插入
        models.data.objects.create(id=item['provinceName'],item=item)
    elif type_ == 'sogou':
        # 直接插入
        models.data.objects.create(id=item['provinceName'],item=item)
    else:
        # 更新插入
        models.data.objects.create(id=item['provinceName'], item=item)
    print(item,'插入成功')

def dxy_spider():
    '''
    丁香园爬取，获取各省份的确诊数，用来做地理热力图
    '''
    url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'
    r = requests.get(url)
    r.encoding = 'utf-8'
    res = re.findall('tryTypeService1 =(.*?)}catch', r.text, re.S)
    if res:
        # 获取数据的修改时间
        time_result = json.loads(res[0])
    res = re.findall('getAreaStat =(.*?)}catch', r.text, re.S)
    if res:
        # 获取省份确诊人数数据
        all_result = json.loads(res[0])
    for times in time_result:
        for item in all_result:
            print(item, '插入成功')
            if times['provinceName'] == item['provinceName']:
                # 因为省份确诊人数的部分没有时间，这里将时间整合进去
                item['createTime'] = times['createTime']
                item['modifyTime'] = times['modifyTime']
                insert_item(item,'dxy_map')

def sogou_spider():
    '''
    搜狗爬虫，获取所有确诊数、治愈数等，用在导航栏直接显示
    '''
    url = 'http://sa.sogou.com/new-weball/page/sgs/epidemic'
    r = requests.get(url=url)
    sum_res = re.findall('"domesticStats":({"tim.*?}})',r.text)
    if sum_res:
        sum_result = json.loads(sum_res[0])
        # 增加一个爬取时间字段
        sum_result['crawl_time'] = int(time.time())
        insert_item(sum_result,'sogou')

def baidu_spider():
    '''
    百度爬虫，爬取历史数据，用来画折线图
    '''
    url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia'
    r = requests.get(url=url)
    res = re.findall('"degree":"3408"}],"trend":(.*?]}]})',r.text,re.S)
    data = json.loads(res[0])
    insert_item(data,'baidu_line')

if __name__ == '__main__':
    dxy_spider()
    sogou_spider()
    baidu_spider()