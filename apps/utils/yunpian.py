# -*- coding:utf-8 -*-
__author__ = "leo"

import json

import requests


class YunPian:
    """云片网短信验证"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, mobile, code):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "云片网模板文件内容{code}".format(code=code),
        }

        response = requests.post(self.single_send_url, data=params)
        return_dict = json.loads(response.text)
        return return_dict


if __name__ == '__main__':
    yunpian = YunPian("云片网的api_key")
    yunpian.send_sms("手机号码", "验证码")