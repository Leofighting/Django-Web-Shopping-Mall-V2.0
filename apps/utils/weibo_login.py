# -*- coding:utf-8 -*-
__author__ = "leo"
import requests


def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_uri = "https://47.92.87.172:8000/complete/weibo/"
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={redirect_uri}".format(
        client_id="", redirect_uri=redirect_uri)
    return auth_url


def get_access_token(code=""):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    re_dict = requests.post(access_token_url, data={
        "client_id": "",
        "client_secret": "",
        "grant_type":"",
        "code": code,
        "redirect_uri": ""
    })
    return re_dict


def get_user_info(access_token="", uid=""):
    user_url = "https://api.weibo.com/2/users/show.json?access_token={token}&uid={uid}".format(
        token=access_token, uid=uid
    )


