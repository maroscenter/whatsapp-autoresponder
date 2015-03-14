#!/usr/bin/python

import log
from layer import WaarLayer
from yowsup.stacks import YowStackBuilder
from yowsup.layers.auth import AuthError
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers import YowLayerEvent

logger = log.init_logger("run")
credentials = ("XXXXXXXXXXXX", "XXXXXXXXXXXXXXXXXXXXXXXXXXXX")

if __name__ == "__main__":
    stackBuilder = YowStackBuilder()
    stack = stackBuilder.pushDefaultLayers().push(WaarLayer).build()
    stack.setCredentials(credentials)
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
    try:
        stack.loop()
    except AuthError as e:
        logger.info("[Auth Error, reason %s ]" % e)