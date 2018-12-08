#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module"""

import aiohttp
import asyncio
import random
import sys
import time

from configparser import ConfigParser

from manager import Manager
from chat import Chat
from proxy import ProxyDB

manager = Manager()
if manager.enable_proxies:
    proxies = ProxyDB(manager.used_timeout, manager.banned_timeout)

# Replies parser
d = ConfigParser()
d.read(manager.responses_data)
replies = dict((section, dict(d.items(section))) for section in d.sections())

# Omegle chat servers
servers = ["front1", "front2", "front3", "front4",
           "front5", "front6", "front7", "front8",
           "front9", "front10", "front11", "front12",
           "front13", "front14", "front15", "front16",
           "front17", "front18", "front19", "front20",
           "front21", "front22", "front23", "front24",
           "front25", "front26", "front27", "front28",
           "front29", "front30", "front31", "front32"]


async def load_proxies():
    if manager.proxy_source:
        while 1:
            manager.logger.debug("Loading proxies")
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(manager.proxy_source) as r:
                        resp = await r.text()
            except Exception:
                continue
            else:
                proxies.add(resp.split("\n"))
                manager.logger.debug("Proxies loaded")
                await asyncio.sleep(10 * 60)


async def stats():
    while 1:
        m, s = divmod(time.time() - manager.start, 60)
        h, m = divmod(m, 60)
        runtime = "%d:%02d:%02d" % (h, m, s)

        if manager.debug:
            await asyncio.sleep(1)
        else:
            sys.stderr.write("\x1b[2J\x1b[H\n\n")
            data = """
        Statistics
. Script Runtime: {}
. Chats Active: {}
. Chats Completed: {}
. Chats Blacklisted: {}
. Captchas Solving: {}
. Captchas Successful: {}
. Proxies Loaded: {}
. Proxies Usable: {}
. Proxies Used: {}
. Proxies Banned: {}
""".format(
                runtime,
                manager.active,
                manager.completed,
                manager.blacklisted,
                manager.captchas_solving,
                manager.captchas_successful,
                proxies.loaded_count(),
                proxies.usable_count(),
                proxies.used_count(),
                proxies.banned_count(),
            )
            sys.stdout.write(data)
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()
            await asyncio.sleep(1)


async def start_chat():
    server = random.choice(servers)
    proxy = await proxies.get() if manager.enable_proxies else None
    while 1:
        chat = Chat(manager, server, replies, proxy)
        await chat.start()
        if manager.enable_proxies:
            proxies.set_used(proxy)
            if not chat.connected:
                proxy = await proxies.get()


async def main():
    asyncio.ensure_future(stats())
    if manager.enable_proxies:
        asyncio.ensure_future(load_proxies())
    for i in range(manager.threads):
        asyncio.ensure_future(start_chat())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
