#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Manager module"""

import logging
import sys
import time
import captcha

try:
    import yaml

    with open("omegle.yaml", "r") as f:
        settings = yaml.load(f)
except FileNotFoundError:
    print("No config file (omegle.yaml) in directory")
    sys.exit(0)

FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(format=FORMAT)

start = time.time()


class Manager(object):
    logger = logging.getLogger(__name__)
    debug = settings["debug"]
    if debug:
        logger.setLevel("DEBUG")
    # Main settings
    threads = settings["threads"]
    enable_proxies = settings["enable_proxies"]
    proxy_source = settings["proxy_source"]
    enable_logs = settings["enable_logs"]
    bot_match = settings["bot_match"]
    # Chat timeout settings
    connect_timeout = settings["chat_timeout"]["connect"]
    response_timeout = settings["chat_timeout"]["response"]
    # Proxy timeout settings
    used_timeout = settings["proxy_timeout"]["used"]
    banned_timeout = settings["proxy_timeout"]["banned"]
    reload_timeout = settings["proxy_timeout"]["reload"]
    # Captcha settings
    solve_captchas = settings["captcha"]["solve_captchas"]
    captcha_service = settings["captcha"]["service"]
    api_key = settings["captcha"][captcha_service]["api_key"]
    if captcha_service == "anticaptcha":
        service = captcha.AntiCaptcha(api_key)
    else:
        service = captcha.TwoCaptcha(api_key)
    # Response data
    responses_data = settings["data"]["responses"]
    spam_urls_data = settings["data"]["urls"]
    blacklist =  open(settings["data"]["blacklist"]).read().split('\n')
    # Logging data (TODO)
    chat_logs_data = settings["log"]["chats"]
    event_logs_data = settings["log"]["events"]
    # Statistics
    start = time.time()
    active = 0
    completed = 0
    blacklisted = 0
    captchas_solving = 0
    captchas_successful = 0
