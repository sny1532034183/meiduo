import json

import requests
from django.conf import settings
from urllib.parse import urlencode

class OAuthWeibo(object):
    """ 微博认证辅助工具类 """
    def __init__(self,client_id = None, client_secret = None, redirect_uri = None, state=None):
        self.client_id = client_id or settings.WEIBO_APP_ID
        self.redirect_uri = redirect_uri or settings.WEIBO_APP_KEY
        self.client_secret=client_secret or settings.WEIBO_REDIRECT_URI
        self.state = state

    def get_weibo_url(self):
        """
        获取微博的验证页面链接
        :return:
        """
        data_dict = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state':self.state
        }
        # print(data_dict)
        # 构造微博登录链接
        weibo_url = 'https://api.weibo.com/oauth2/authorize?' + urlencode(data_dict)
        return weibo_url

    def get_access_token(self, code):
        """
        获取微博的accesstoken值
        https://api.weibo.com/oauth2/access_token
        ?client_id=YOUR_CLIENT_ID
        &client_secret=YOUR_CLIENT_SECRET
        &grant_type=authorization_code
        &redirect_uri=YOUR_REGISTERED_REDIRECT_URI
        &code=CODE

        :param code:
        :return:
        """
        # 构造参数
        data_dict = {
            "client_id":self.client_id,
            "client_secret":self.client_secret,
            "grant_type":"authorization_code",
            "redirect_uri":self.redirect_uri,
            "code":code
        }

        # 发送请求
        url = "https://api.weibo.com/oauth2/access_token"
        try:
            response = requests.post(url=url,data=data_dict)

            # 提取数据
            # {
            #     "access_token": "SlAV32hkKG",
            #     "remind_in": 3600,
            #     "expires_in": 3600
            # }
            data = response.text
            data_dict = json.loads(data)
            # access_token = data_dict["access_token"]
            print(data_dict,type(data_dict))
        except:
            raise Exception('微博请求失败')
        # return access_token
        return data_dict
