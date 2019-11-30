#encoding=utf-8
'''
Created on 2019��10��9��
@author: sea
'''
# from com.sea.hhtp.MyHttp import get, post
from utils import httpUtils



print("###################################################")
print("###################################################")
print("################       GET     ####################")
print("###################################################")
print("###################################################")
headers = {
            "user-agent"  : "ad",
            "Appstore-clientType" : "android",
            "Appstore-IMEI" : "123456789000000"
            }

getheader={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
getresult =httpUtils.get("http://192.168.18.129:7016/worktable?page=1&size=2")
print(str(getresult))
print("13213")
print("13213")




print("###################################################")
print("###################################################")
print("################       POST     ###################")
print("###################################################")
print("###################################################")



postresult = httpUtils.post("http://192.168.18.129:7016/worktable/dynamicQueryWithPage",'{"status":"CCD","page":1,"size":2}',{"Content-Type":"application/json"})
print(str(postresult))