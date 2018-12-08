#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Captcha solving module"""

import json
import time

from util import get_request, post_request


class AntiCaptcha(object):
    def __init__(self, api_key):
        self.api_url = "http://api.anti-captcha.com/"
        self.api_key = api_key

    async def get_balance(self):
        fields = {"clientKey": self.api_key}
        response = await post_request(
            f"{self.api_url}/getBalance", json=fields
        )
        errorId = int(response["errorId"])
        if errorId > 1:
            return
        balance = response["balance"]
        return balance

    async def solve_captcha(self, sitekey, pageurl):
        payload = {
            "clientKey": self.api_key,
            "task": {
                "type": "NoCaptchaTaskProxyless",
                "websiteURL": pageurl,
                "websiteKey": sitekey,
            },
            "softId": 0,
            "languagePool": "en",
        }
        response = await post_request(
            f"{self.api_url}/createTask", json=payload
        )
        j = json.loads(response)
        taskId = j["taskId"]
        errorId = int(j["errorId"])
        if errorId > 1:
            return
        payload = {"clientKey": self.api_key, "taskId": taskId}
        time.sleep(10)
        while 1:
            response = await post_request(
                f"{self.api_url}/getTaskResult", json=payload
            )
            j = json.loads(response)
            if j["status"] == "processing":
                time.sleep(5)
            elif errorId > 1:
                return
            else:
                break
        return j["solution"]["gRecaptchaResponse"]


class TwoCaptcha(object):
    def __init__(self, api_key):
        self.api_url = "http://2captcha.com/"
        self.api_key = api_key

    async def solve_captcha(self, googlekey, pageurl):
        payload = {
            "key": self.api_key,
            "method": "userrecaptcha",
            "googlekey": googlekey,
            "pageurl": pageurl,
        }
        response = await post_request(f"{self.api_url}/in.php", data=payload)
        if 'ERROR' not in response:
            cap_id = response.split("|")[-1]
            params = f"key={self.api_key}&action=get&id={cap_id}"
            for i in range(10):
                response = await get_request(
                    f"{self.api_url}/res.php?{params}"
                )
                if response in ["CAPCHA_NOT_READY", "ERROR_NO_SLOT_AVAILABLE"]:
                    time.sleep(5)
                else:
                    answer = response.split("|")[-1]
                    return answer
