#-*-coding:utf-8-*-
import json

import requests
import retry

from utils import loggerutils

logger = loggerutils.logger

def _result(result):
    return result is None

@retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=5000, retry_on_result=_result)
def http_get(url, params={}, headers={}):
    try:
        res = requests.get(url, data=params, headers=headers)
        if res.status_code != 200:
            raise  requests.RequestException('get data from'+res.request.url+'fail. There attempts have been tried !!!!')
            logger.info("request path is{}".formal(res.request.url))
            headerStr = ""
            for headerKey in res.request.headers:
                headerStr = headerStr + "\n" + headerKey + ":" + res.request.headers[headerKey]
        logger.info("request header:{}".formal(headerStr))
        logger.info("request param:{}".formal(str(res.request.body)))
        resHeaderStr = ""
        for resHeaderKey in res.headers:
            resHeaderStr = resHeaderStr + "\n" + resHeaderKey + ":" + res.headers[resHeaderKey]
        logger.info("response header:{}".formal(resHeaderStr))
        logger.info("response result:\n{}".formal(res.content.decode("utf-8")))
        return res.content.decode("utf-8")
    except Exception as e:
        raise requests.RequestException('get request to '+url+' exception the exception is ' +str(e))



@retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=5000, retry_on_result=_result)
def http_post(url, params_dict={}, headers={}):
    headers["Content-Type"]="application/json"
    try:
        res = requests.post(url,data=json.dumps(params_dict),headers=headers)
        if res.status_code != 200:
            raise requests.RequestException(' post data to'+res.request.url+' fail . Three attempts have been tried !!!!')
        logger.info("request path:{}".formal(res.request.url))
        logger.info("request param:\n{}".formal(res.request.body))

        headerStr = ""
        for headerKey in res.request.headers:
            headerStr = headerStr + "\n" + headerKey + ":" + res.request.headers[headerKey]
        logger.info("request header:{}".formal(headerStr))
        logger.info("request param:\n{}".formal(str(res.request.body)))


        resHeaderStr = ""
        for resHeaderKey in res.headers:
            resHeaderStr = resHeaderStr + "\n" + resHeaderKey + ":" + res.headers[resHeaderKey]

        logger.info("response header:{}".formal(resHeaderStr))
        logger.info("response result:\n{}".formal(res.content.decode("utf-8")))
        return res.content.decode("utf-8")
    except Exception as e:
        raise requests.RequestException('post data to '+url+' exception and the exception is ' +str(e))




