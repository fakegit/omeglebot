#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Chat module"""

import asyncio
import json
import random
import time

import handler
import util
import typo


class Chat(object):
    session_id = None
    connected = False
    disconnected = False
    completed = False
    replying = False
    recaptcha_required = False
    reply_id = 1

    def __init__(self, manager, server, replies, proxy=None):
        self.manager = manager
        self.server = server
        self.replies = replies[random.choice(list(replies.keys()))]
        self.proxy = f"http://{proxy}" if proxy else None
        self.events = asyncio.Queue()
        self.handler = handler.Handler()

    async def start(self):
        self.reply = dict(
            (int(r), self.replies[r]) for r in self.replies.keys()
        )
        self.last_reply_id = sorted(self.reply.keys())[-1]
        await self.connect()

    async def connect(self):
        self.log(f"Connecting with proxy {self.proxy}")
        randid = "".join(
            random.choice("23456789ABCDEFGHJKLMNPQRSTUVWXYZ") for x in range(8)
        )
        topics = json.dumps(self.manager.topics.split(','))
        page = (
            f"/start?"
            f"caps=recaptcha2&firstevents=1&spid=&randid={randid}&"
            f"lang={self.manager.chat_language}&topics={topics}"
        )
        j = await self.open_page(page)
        if j:
            if "clientID" in j:
                self.session_id = j["clientID"]
                events = j["events"]
                await self.process_events(events)
                poll = asyncio.ensure_future(self.poll_events())
                consume = asyncio.ensure_future(self.consume())
                self.manager.active += 1
                await self.pingback()
                self.manager.active -= 1
                poll.cancel()
                consume.cancel()

    async def poll_events(self):
        while not self.disconnected:
            events = await self.open_page("events")
            if events:
                await self.events.put(events)
            await asyncio.sleep(2)

    async def consume(self):
        while not self.disconnected:
            events = await self.events.get()
            await self.process_events(events)

    async def pingback(self):
        self.timeout = self.manager.response_timeout + time.time()
        while not self.disconnected:
            if self.timeout <= time.time():
                self.log("chat time-out")
                await self.disconnect()
                self.disconnected = True
            await asyncio.sleep(1)

    async def process_events(self, events):
        for event in events:
            if len(event) > 1:
                await self.handler.fire(self, event[0], event[1:])
            else:
                await self.handler.fire(self, event[0])

    async def open_page(self, page, payload={}):
        if self.session_id:
            payload["id"] = self.session_id
        try:
            response = await util.post_request(
                        f"http://{self.server}.omegle.com/{page}",
                        proxy=self.proxy,
                        data=payload,
                        timeout=self.manager.connect_timeout,
            )
            return json.loads(response)
        except BaseException:
            pass

    async def recaptcha(self, solution):
        await self.open_page("recaptcha", payload={"response": solution})

    async def say(self, message):
        await self.open_page("send", payload={"msg": message})

    async def typing(self):
        await self.open_page("typing")

    async def stoppedtyping(self):
        await self.open_page("stoppedtyping")

    async def disconnect(self):
        await self.open_page("disconnect")
        self.disconnected = True

    async def send_reply(self):
        while self.replying:
            await asyncio.sleep(1)
        self.replying = True
        if self.reply_id <= self.last_reply_id:
            try:
                segments = self.reply[self.reply_id].split("\n")
            except KeyError:
                pass
            else:
                for segment, reply in enumerate(segments):
                    if len(self.manager.reply_delay.split(",")) == 2:
                        start, end = [
                            float(x) for x in self.manager.reply_delay.split(",")
                        ]
                    else:
                        start, end = (1.0, 3.0)
                    await asyncio.sleep(random.uniform(1.0, 3.0))
                    await self.prepare_reply(segment, reply)
        if self.reply_id == self.last_reply_id:
            self.log(f"conversation completed")
            self.manager.completed += 1
            await self.disconnect()
        else:
            self.reply_id += 1
            self.replying = False

    async def prepare_reply(self, segment, reply):
        segment += 1
        safe = {
            "bot_match": "[bot_match]"
        }
        reply = reply.replace(safe["bot_match"], self.manager.bot_match)
        reply = typo.generate_typos(typo.spin_content(reply), safe)
        self.log(f"simulating typing for reply[{self.reply_id}][{segment}]")
        asyncio.ensure_future(self.typing())
        wait_for = float(len(reply)) / random.uniform(6.0, 11.0)
        await asyncio.sleep(wait_for)
        self.log(f"sending reply[{self.reply_id}][{segment}]")
        await self.say(reply)
        self.log(f"sent reply[{self.reply_id}][{segment}]")

    def log(self, message):
        self.manager.logger.debug(f"{self.session_id} {message}")
