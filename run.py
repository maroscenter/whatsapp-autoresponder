#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from ConfigParser import SafeConfigParser
import sys

from yowsup.stacks import YowStackBuilder
from yowsup.layers.auth import AuthError
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers import YowLayerEvent

import log
from layer import WaarLayer


logger = log.init_logger(__name__)

if __name__ == "__main__":
    config_parser = SafeConfigParser()
    config_parser.read(os.path.join(sys.path[0], "waar.cfg"))
    stack_builder = YowStackBuilder()
    stack = stack_builder.pushDefaultLayers().push(WaarLayer).build()
    credentials = (config_parser.get("login", "phone"), config_parser.get("login", "password"))
    stack.setCredentials(credentials)
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
    try:
        stack.loop()
    except AuthError as error:
        logger.info("[AUTH ERROR, REASON: %s ]", error)
    except KeyboardInterrupt:
        logger.info("[RESPONDER SHUT DOWN BY USER]")
        sys.exit(0)
