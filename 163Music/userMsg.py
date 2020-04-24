#-*-coding:utf-8-*-
from bs4 import BeautifulSoup

import requests
from utils import mysqlUtil

def query_user(self, http_type, ip, port):
    # 判断ip是否可用
    http_url = "https://music.163.com/weapi/user/getfolloweds?csrf_token="

    if http_type == 'HTTP':
        use_http_type = 'http'
    else:
        use_http_type = 'https'

    proxy = {use_http_type: ip + ":" + port}
    # proxy = {use_http_type: "{0}://{1}:{1}".format(use_http_type, ip, port)}
    try:
        response = requests.get(http_url, proxies=proxy)
    except Exception as e:
        print("无效的ip:", ip, e)
        self.delete_ip(ip)
        return False
    else:
        code = response.status_code
        if 200 <= code < 300:
            print("有效的ip:", ip)
            return True
        else:
            print("无效的ip:", ip)
            self.delete_ip(ip)
            return False



def query_user_message():
    # 爬取西刺网代理ip
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    for i in range(1, 100):
        print("====================", i)
        re = requests.get("https://music.163.com/#/user/fans?id=1452176465".format(i), headers=headers)
        text = re.text
        soup = BeautifulSoup(text)
        soup1 = BeautifulSoup(soup.text)
        soup2 = BeautifulSoup(soup1.text)
        tr_list = soup.select("tr")
        tr_list = tr_list[1:]
        for td_list in tr_list:
            td_ip = td_list.select("td")[1].get_text()
            td_port = td_list.select("td")[2].get_text()
            http_type = td_list.select("td")[5].get_text()
            speed = float((td_list.select("td")[6].div.get('title'))[:1])
            if speed > 1:
                continue
            insert_sql = "insert into ip_list(http_type,ip,port,speed) values(%s,%s,%s,%s)"
            mysqlUtil.insertone(insert_sql, (http_type, td_ip, td_port, speed))
            print(td_ip)


if __name__ == "__main__":
    # crawl_ips()
    query_user_message()
