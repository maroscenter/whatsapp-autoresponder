#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
from ConfigParser import SafeConfigParser

import sys


def init_logger(name):
    config_parser = SafeConfigParser()
    config_parser.read(os.path.join(sys.path[0], "waar.cfg"))
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    log_file = config_parser.get("path", "logfile")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
