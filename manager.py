#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys
import time
import captcha

try:
    import yaml

    with open("omegle.yaml", "r") as f:
        settings = yaml.load(f)
except FileNotFoundError:
    print("No config file in directory")
    sys.exit(0)


FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(format=FORMAT)

start = time.time()


class Manager(object):
    logger = logging.getLogger(__name__)
    verbosity = settings["verbosity"]
    if verbosity == 0:
        logger.setLevel("NOTSET")
    if verbosity == 1:
        logger.setLevel("CRITICAL")
    if verbosity == 2:
        logger.setLevel("ERROR")
    if verbosity == 3:
        logger.setLevel("WARNING")
    if verbosity == 4:
        logger.setLevel("INFO")
    if verbosity == 5:
        logger.setLevel("DEBUG")
    # Main settings
    threads = settings["threads"]
    proxy_source = settings["proxy_source"]
    enable_logs = settings["enable_logs"]
    solve_captchas = settings["solve_captchas"]
    # Chat timeout settings
    connect_timeout = settings["chat_timeout"]["connect"]
    response_timeout = settings["chat_timeout"]["response"]
    # Proxy timeout settings
    used_timeout = settings["proxy_timeout"]["used"]
    banned_timeout = settings["proxy_timeout"]["banned"]
    reload_timeout = settings["proxy_timeout"]["reload"]
    # Captcha settings
    captcha_service = settings["captcha"]["service"]
    if captcha_service == "anticaptcha":
        api_key = (
            captcha_service["anticaptcha"]["api_key"]
        )
        service = captcha.AntiCaptcha(api_key)
    else:
        api_key = (
            captcha_service["2captcha"]["api_key"]
        )
        service = captcha.TwoCaptcha(api_key)
    # Response data
    responses_data = settings["data"]["responses"]
    spam_urls_data = settings["data"]["urls"]
    # Logging data
    chat_logs_data = settings["log"]["chats"]
    event_logs_data = settings["log"]["events"]
    # Statistics
    start = time.time()
    active = 0
    completed = 0
    blacklisted = 0
    captchas_solving = 0
    captchas_successful = 0
