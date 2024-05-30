import requests, json
from django.conf import settings
from django.utils import timezone
from datetime import date, time, timedelta
from typing import Tuple, List
from django.http import HttpRequest
from dataclasses import dataclass
import logging


class WeixinApiError(Exception):
    pass

class WxLogin:

    @staticmethod
    def jscode2session(js_code: str) -> Tuple[str, str, str]:
        params = {
            "appid": settings.WX_APP_ID,  # 小程序的 ID
            "secret": settings.WX_APP_SECRET,  # 小程序的 secret
            "js_code": js_code,
            "grant_type": "authorization_code",
        }
        resp = requests.get(
            "https://api.weixin.qq.com/sns/jscode2session",
            params=params,
            timeout=3,
            verify=False,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("openid"), data.get("session_key"), data.get("unionid")


    ACCESS_TOKEN = None
    ACCESS_EXPRIES_TIME = None

    @staticmethod
    def get_access_token():
        logging.debug(f"==========get_access_token,{WxLogin.ACCESS_TOKEN},{WxLogin.ACCESS_EXPRIES_TIME}")
        if WxLogin.ACCESS_TOKEN and WxLogin.ACCESS_EXPRIES_TIME and WxLogin.ACCESS_EXPRIES_TIME < timezone.now():
            return WxLogin.ACCESS_TOKEN

        params = {
            "grant_type": "client_credential",
            "appid": settings.WX_APP_ID,
            "secret": settings.WX_APP_SECRET,
        }
        resp = requests.get("https://api.weixin.qq.com/cgi-bin/token", params=params)

        resp.raise_for_status()

        data = resp.json()

        errcode = data.get("errcode")
        if errcode:
            raise WeixinApiError("get_access_token", errcode, data.get("errmsg"))

        access_token = data["access_token"]
        expires_in = data["expires_in"]
        expires_time = timezone.now() + timedelta(seconds=expires_in)
        WxLogin.ACCESS_TOKEN = access_token
        WxLogin.ACCESS_EXPRIES_TIME = WxLogin.ACCESS_EXPRIES_TIME
        return WxLogin.ACCESS_TOKEN

    @staticmethod
    def get_phone_number(code):
        access_token = WxLogin.get_access_token()
        params = {"access_token": access_token}
        print('debug _ ', params, code)
        hdeaders = {"Content-Type": "application/json"}

        resp = requests.post(
            "https://api.weixin.qq.com/wxa/business/getuserphonenumber",
            params=params,
            data= json.dumps({"code": code}),
            headers=hdeaders
        )
        resp.raise_for_status()
        data = resp.json()
        logging.debug(f"==========get_phone_number {data}")
        errcode = data.get("errcode")
        if errcode:
            raise WeixinApiError("get_phone_number", errcode, data.get("errmsg"))

        phone_info = data.get("phone_info")
        logging.debug(f"===========phone_info {phone_info}")

        return phone_info.get("countryCode"), phone_info.get("purePhoneNumber")


    @staticmethod
    def get_stable_token():
        logging.debug(f"==========get_stable_token,{WxLogin.ACCESS_TOKEN},{WxLogin.ACCESS_EXPRIES_TIME}")
        if WxLogin.ACCESS_TOKEN and WxLogin.ACCESS_EXPRIES_TIME and WxLogin.ACCESS_EXPRIES_TIME < timezone.now():
            return WxLogin.ACCESS_TOKEN

        params = {
            "grant_type": "client_credential",
            "appid": settings.WX_APP_ID,
            "secret": settings.WX_APP_SECRET,
        }
        resp = requests.post("https://api.weixin.qq.com/cgi-bin/stable_token", json=params)



        resp.raise_for_status()

        data = resp.json()

        errcode = data.get("errcode")
        if errcode:
            raise WeixinApiError("get_access_token", errcode, data.get("errmsg"))

        access_token = data["access_token"]
        expires_in = data["expires_in"]
        expires_time = timezone.now() + timedelta(seconds=expires_in)
        WxLogin.ACCESS_TOKEN = access_token
        WxLogin.ACCESS_EXPRIES_TIME = WxLogin.ACCESS_EXPRIES_TIME
        return ACCESS_TOKEN


    @staticmethod
    def clear_quota():
        access_token = WxLogin.get_stable_token()
        params = {"access_token": access_token,
                  "appid": settings.WX_APP_ID
                  }

        resp = requests.post(
            "https://api.weixin.qq.com/cgi-bin/clear_quota",
            params=params,
            json={"appid": settings.WX_APP_ID},
        )
        resp.raise_for_status()
        data = resp.json()
        logging.debug(f"==========clear_quota {data}")
        errcode = data.get("errcode")
        if errcode:
            raise WeixinApiError("clear_quota", errcode, data.get("errmsg"))


        return "OK"

@dataclass
class WeiXinSideUserInfo:
    openid: str
    session_key: str
    unionid: int
    country_code: str
    phone_number: str

def wx_login_process(request: HttpRequest) -> tuple[bool, WeiXinSideUserInfo]:
    try:
        data = json.loads(request.body)
        phone_data = data["verify"]
        code = phone_data["code"]
        login_code = phone_data["loginCode"]
    except Exception as err:
        return False, "weixin login api failed, parameter_error, body:{}".format(request.body)
    try:
        openid, session_key, unionid = WxLogin.jscode2session(login_code)
        country_code, phone_number = WxLogin.get_phone_number(code)
    except json.JSONDecodeError as err:
        return False, 'login error json decode error:{}'.format(err)
    except requests.HTTPError as err:
        return False, 'login error http error:{}'.format(err)
    except WeixinApiError as err:
        return False, 'login error weixin api error:{}'.format(err)
    except Exception as err:
        return False, 'login error:{}'.format(err)
    collect_wx_login_info = WeiXinSideUserInfo(openid, session_key, unionid, country_code, phone_number)
    return True , collect_wx_login_info