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
        fields = {
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
            f"{self.api_url}/createTask", json=fields
        )
        j = json.loads(response)
        taskId = j["taskId"]
        errorId = int(j["errorId"])
        if errorId > 1:
            return
        fields = {"clientKey": self.api_key, "taskId": taskId}
        time.sleep(10)
        for i in range(10):
            response = await post_request(
                f"{self.api_url}/getTaskResult", json=fields
            )
            j = json.loads(response)
            if j["status"] == "processing":
                time.sleep(5)
            else:
                break
        return j["solution"]["gRecaptchaResponse"]


class TwoCaptcha(object):
    def __init__(self, api_key):
        self.api_url = "http://2captcha.com/"
        self.api_key = api_key

    async def solve_captcha(self, googlekey, pageurl):
        fields = {
            "key": self.api_key,
            "method": "userrecaptcha",
            "googlekey": googlekey,
            "pageurl": pageurl,
        }
        response = await get_request(f"{self.api_url}/in.php", payload=fields)
        if 'ERROR' not in response:
            cap_id = response.split("|")[-1]
            fields = {"key": self.api_key, "action": "get", "id": cap_id}
            time.sleep(15)
            for i in range(10):
                response = await get_request(
                    f"{self.api_url}/res.php", payload=fields
                )
                if response in ["CAPCHA_NOT_READY", "ERROR_NO_SLOT_AVAILABLE"]:
                    time.sleep(5)
                else:
                    answer = response.split("|")[-1]
                    return answer
