import asyncio
import aiohttp

class Web(object):

    def __init__(self, proxy=None, timeout=30, headers={}):
        self.headers = headers
        self.timeout = timeout
        self.proxy = proxy
        self.session = aiohttp.ClientSession()

    def get(self, url, **kwargs):
        timeout = kwargs.get('timeout', self.timeout)
        json = kwargs.get('json', False)
        binary = kwargs.get('binary', False)
        async with self.session as s:
            async with s.get(url, proxy=self.proxy) as r:
                if json:
                    content = await r.json()
                elif binary:
                    content = await r.content()
                else:
                    content = await r.text()
            return content

    def post(self, url, payload, **kwargs):
        timeout = kwargs.get('timeout', self.timeout)
        json = kwargs.get('json', False)
        binary = kwargs.get('binary', False)
        async with self.session as s:
            async with s.get(url, data=payload, proxy=self.proxy) as r:
                if json:
                    content = await r.json()
                elif binary:
                    content = await r.content()
                else:
                    content = await r.text()
            return content

    def send(self, url, method='GET', **kwargs):
        timeout = kwargs.get('timeout', self.timeout)
        prepped = Request(method,
                          url,
                          params=kwargs.get('params',None),
                          data=kwargs.get('fields',None),
                          files=kwargs.get('files',None),
                          headers=kwargs.get('headers',self.headers)
        ).prepare()

        try:
            response = self.session.send(
                           prepped,
                           timeout=timeout
            )
        except Exception, e:
            pass #raise e
        else:
            if response:
                return response


async def main():
    session = aiohttp.ClientSession()
    async with session as s:
        async with s.get("http://www.google.com/") as r:
            content = await r.text()
        return content

web = Web()
print(asyncio.get_event_loop().run_until_complete(main()))