#-*-coding:utf-8-*-
import requests

class httpUtils:
    def get(self, url, params={}, headers={}):
        res = requests.get(url,data=params,headers=headers)
        print("request path:" +res.request.url)
        headerStr = ""
        for headerKey in res.request.headers:
            headerStr = headerStr + "\n" + headerKey + ":" + res.request.headers[headerKey]
        print("request header:" + headerStr)
        print("request param:" + res.request.body)

        resHeaderStr = ""
        for resHeaderKey in res.headers:
            resHeaderStr = resHeaderStr + "\n" + resHeaderKey + ":" + res.headers[resHeaderKey]
        print("响应头信息：" + resHeaderStr)
        print("返回结果：\n" + res.content.decode("utf-8"))
        return res

    def post(self, url, params={}, headers={}):
        res = requests.post(url, data=params, headers=headers)
        print("请求路径：" + res.request.url)
        headerStr = ""
        for headerKey in res.request.headers:
            headerStr = headerStr + "\n" + headerKey + ":" + res.request.headers[headerKey]
        print("请求头信息：" + headerStr)
        print("请求参数：\n" + res.request.body)

        resHeaderStr = ""
        for resHeaderKey in res.headers:
            resHeaderStr = resHeaderStr + "\n" + resHeaderKey + ":" + res.headers[resHeaderKey]
        print("响应头信息：" + resHeaderStr)
        print("返回结果：\n" + res.content.decode("utf-8"))
        return res