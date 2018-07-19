#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utility functions"""

import aiohttp


async def post_request(url, data=None, json=None, proxy=None, timeout=180):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                url,
                data=data,
                json=json,
                proxy=proxy,
                timeout=timeout,
            ) as r:
                return await r.text()
        except BaseException as e:
            raise e


async def get_request(url, data=None, json=None, proxy=None, timeout=180):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url,
                data=data,
                json=json,
                proxy=proxy,
                timeout=timeout,
            ) as r:
                return await r.text()
        except BaseException as e:
            raise e
