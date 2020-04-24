#-*-coding:utf-8-*-
from bs4 import BeautifulSoup

import requests
from utils import mysqlUtil


def crawl_ips():
    # 爬取西刺网代理ip
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
    }
    for i in range(1, 20):
        print("====================", i)
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
        text = re.text
        soup = BeautifulSoup(text)
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


class GetIp(object):
    def delete_ip(self, ip):
        #从数据库中删除无效的ip
        delete_sql = "delete from ip_list where ip = %s"
        mysqlUtil.execute(delete_sql, ip)

    def judge_ip(self, http_type, ip, port):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        }
        # 判断ip是否可用
        http_url = "http://zz.lianjia.com/ershoufang/erqi"

        if http_type == 'HTTP':
            use_http_type = 'http'
        else:
            use_http_type = 'https'

        proxy = {use_http_type: ip + ":" + port}
        # proxy = {use_http_type: "{0}://{1}:{1}".format(use_http_type, ip, port)}
        try:
            response = requests.get(http_url, proxies = proxy, headers=headers)
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

    def get_ip(self):
        # 从数据库随机取一个可用的ip
        random_sql = " select http_type,ip,port from ip_list order by rand() limit 1 "
        result = mysqlUtil.queryone(random_sql)
        # for ip_info in result:
        http_type = result['http_type']
        ip = result['ip']
        port = result['port']
        judge_re = self.judge_ip(http_type, ip, port)
        if judge_re:
            if http_type == 'HTTP':
                use_http_type = 'http'
            else:
                use_http_type = 'https'

            return {use_http_type: ip + ":" + port}
            # return http_type + "://" + ip + ":" + port
        else:
            return self.get_ip()






if __name__ == "__main__":
    crawl_ips()
    # getip = GetIp()
    # print(getip.get_ip())
