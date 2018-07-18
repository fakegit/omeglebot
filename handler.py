import aiohttp
import asyncio
import time


class UnhandledEvent(Exception):
    pass


class EventHandler(object):
    async def fire(self, client, event, var=None):
        if hasattr(self, event):
            await getattr(self, event)(client, var)
        else:
            print(UnhandledEvent(f"{event} not handled"))


class Handler(EventHandler):
    async def waiting(self, client, var):
        client.log(f"waiting")

    async def connected(self, client, var):
        client.log(f"connected")
        client.connected = True
        await client.send_reply()

    async def gotMessage(self, client, message):
        client.timeout = client.manager.response_timeout + time.time()
        self.stranger_typing = False
        if message:
            # client.manager.blacklisted += 1
            client.log(f"received message")
            await client.send_reply()

    async def strangerDisconnected(self, client, var):
        client.disconnected = True
        client.log(f"stranger disconnected")

    async def typing(self, client, var):
        client.log(f"stranger is typing")
        self.stranger_typing = True

    async def stoppedTyping(self, client, var):
        client.log(f"stranger stopped typing")
        self.stranger_typing = False

    async def recaptchaRequired(self, client, var):
        client.manager.captchas_solving += 1
        client.log(f"reCAPTCHA required")
        pageurl = f"http://{client.server}.omegle.com/"
        sitekey = var[0]
        try:
            solution = client.manager.service.solve_captcha(sitekey, pageurl)
        except BaseException:
            client.disconnected = True
        else:
            if solution:
                client.recaptcha_required = True
                client.log(f"reCAPTCHA solution received")
                await client.recaptcha(j["solution"])
                client.log(f"reCAPTCHA solution sent")
                client.manager.captchas_successful += 1
            else:
                client.disconnected = True
        client.manager.captchas_solving -= 1

    async def recaptchaRejected(self, client, var):
        client.manager.captchas_successful -= 1
        client.disconnected = True

    async def identDigests(self, *args):
        pass

    async def statusInfo(self, *args):
        pass
