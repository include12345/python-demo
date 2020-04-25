#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
from utils import mysqlUtil
from utils import ipProxyUtil

import re
import json



def get_hourse_href():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    for i in range(1, 2):
        url = 'http://zz.lianjia.com/ershoufang/binjiang/pg' + str(i) + '/'
        re = requests.get(url, headers=headers)
        text = re.text
        soup = BeautifulSoup(text, "html.parser")
        for title in soup.find_all('div', 'title'):
            print(title.a)


def get_row_lianjia():
    query_sql = "select id from lianjia order by id desc limit 1"
    result = mysqlUtil.queryone(query_sql)
    if result is None:
        return 1
    else:
        return int(result) + 1



def get_house_info(id, row):
    while id <= row:
        query_sql = "select * from lianjia where id = %s"
        result = mysqlUtil.queryone(query_sql, id)
        url = None
        if result is None:
            return
        else:
            url = result['url']
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        }
        rep = requests.get(url, proxies={'http': '39.137.69.6:8080'}, headers=headers)
        text = rep.text
        soup = BeautifulSoup(text, "html.parser")
        print(soup)
        id += 1
        communityName = soup.find_all('div', 'communityName')
        context = communityName[0].contents[2]
        print(context.get_text()) # todo insert sql
        sublocation = soup.find_all('div', 'areaName')  # 获取链接
        test = sublocation[0].contents[2].contents[2]
        print(test.get_text()) # todo insert sql

        base = soup.find_all('div', 'base')
        for content in base[0].contents[3].contents[1].contents:
            if content == u'\n':
                continue
            print(content.get_text()) # todo insert sql
        transaction = soup.find_all('div', 'transaction')
        for content in transaction[0].contents[3].contents[1].contents:
            if content == u'\n':
                continue
            label = content.get_text().split('\n')
            print(label[2])

        introContent = soup.find_all('div', 'introContent showbasemore')
        for content in introContent[0].contents:
            if content == u'\n' or content.get_text().find('房源标签') >= 0 or content.get_text().find('展开更多信息') >= 0 or content.get_text().find('注：') >= 0:
                continue
            label = content.contents[3].contents[0].split('\n')
            print(label[2])

        newCalculator = soup.find_all('div', attrs={"class":"new-calculator VIEWDATA", "data-shoufu": re.compile('totalLoan')})
        shoufu = newCalculator[0].get('data-shoufu')
        print(json.loads(shoufu))
        # print(json.loads(test).get('totalLoan'))
        # print(test)

def get_hourse(location, current_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    url = 'http://zz.lianjia.com/ershoufang/' + location
    # getip = ipProxyUtil.GetIp()
    # proxyurl = getip.get_ip()
    rep = requests.get(url, proxies = {'http': '39.137.69.6:8080'}, headers=headers)
    text = rep.text
    soup = BeautifulSoup(text, "html.parser")
    current_page = 1
    try:
        error = soup.title.text
        if error == u"验证异常流量-链家网":
            print("ip被封")
        else:
            pass
    except:
        pass

    for link in soup.find_all('div', 'resultDes clear'):
        context = link.get_text()
        total_house = re.findall(r"\d+\.?\d*", context)[0]  # 总共有多少套房子
        print(location + '一共有' + total_house + '套房子')
        total_page = int(total_house) / 30 + 1
        while current_page <= total_page:
            pgurl = 'http://zz.lianjia.com/ershoufang/' + location + '/pg' + str(current_page) + '/'
            subrep = requests.get(pgurl, proxies={'http': '39.137.69.6:8080'}, headers=headers)
            subtext = subrep.text
            subsoup = BeautifulSoup(subtext, "html.parser")
            id = current_id
            for price in subsoup.find_all('div', 'totalPrice'):
                unit_price = price.get_text()
                unit_price = unit_price[:-1]  # 把最后的一个万字去掉
                insert_sql = "insert into lianjia(id, total_price, location, ctime) values(%s, %s, %s, CURRENT_TIMESTAMP)"
                mysqlUtil.insertone(insert_sql, (id, unit_price, location))
                print('price', id, unit_price)
                id += 1

            id = current_id
            for houseInfo in subsoup.find_all('div', 'houseInfo'):
                context = houseInfo.get_text()
                village = context.split('|')[0]
                house_type = context.split('|')[1]
                square = context.split('|')[2][:3]
                orientation = context.split('|')[3]
                decorate = ''
                if u'别墅' in house_type:
                    house_type = context.split('|')[2]
                    square = context.split('|')[3][:-3]  # 把平米两个字去掉
                    orientation = context.split('|')[4]
                if len(context.split("|")) >= 5:
                    decorate = context.split('|')[4]
                update_sql = "update lianjia set village = %s, house_type = %s, square = %s, orientation = %s, decorate = %s where id = %s"
                mysqlUtil.execute(update_sql, (village, house_type, square, orientation, decorate, id))

                print('houseInfo', id, village, house_type, square, orientation, decorate)
                id += 1
            id = current_id
            for unitPrice in subsoup.find_all('div', 'unitPrice'):  # 单价的信息
                unit_price = unitPrice.get_text()
                unit_price = re.findall(r"\d+\.?\d*", unit_price)[0]
                update_sql = "update lianjia set per_square = %s, page = %s where id = %s"
                mysqlUtil.execute(update_sql, (unit_price, current_page, id))
                print('unitPrice', id, unit_price, current_page)
                id += 1
            id = current_id
            for href in subsoup.find_all("a", attrs={"target": "_blank", 'class': "title"}):  # 获取链接
                url_text = href.get('href')
                target = href.get_text()
                update_sql = "update lianjia set url = %s, name =%s where id = %s"
                mysqlUtil.execute(update_sql, (url_text, target, id))
                print('href', id, url_text)
                id += 1
            id = current_id
            for followInfo in subsoup.find_all('div', 'followInfo'):  # 单价的信息
                follow = followInfo.get_text()
                update_sql = "update lianjia set follow = %s, mtime = CURRENT_TIMESTAMP where id = %s"
                mysqlUtil.execute(update_sql, (follow, id))
                print('href', id, follow)
                id += 1
            current_page += 1
            current_id = id
if __name__ == "__main__":
    # crawl_ips()
    # n = get_row_lianjia()
    # print(get_hourse('jinshui', n))
    # n = get_row_lianjia()
    # print(get_hourse('huiji', n))
    #
    # n = get_row_lianjia()
    # print(get_hourse('zhongyuan', n))
    #
    # n = get_row_lianjia()
    # print(get_hourse('hangkonggangqu', n))
    #
    # n = get_row_lianjia()
    # print(get_hourse('gaoxin9', n))
    #
    # n = get_row_lianjia()
    # print(get_hourse('jingkaiqu', n))
    get_house_info(1, 91283)
