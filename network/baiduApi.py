# -*- coding: utf-8 -*-n()
import urllib, urllib2,json
from logger import logger

class BaiduApi():
    def __init__(self):
        logger.info('初始化【BaiduApi】')
        self.token = ''
    def init_token(self): 
        apiKey = "Qa6vDpKF8eFiWjXFrC3erMcl" 
        secretKey = "cf8cdca9e7a792919bf24756ce7f9a0a" 
        
        auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey; 
        
        res = urllib2.urlopen(auth_url) 
        json_data = res.read() 
        self.token = json.loads(json_data)['access_token']
    def get_token(self):
        return self.token