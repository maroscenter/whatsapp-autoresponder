#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
from ConfigParser import SafeConfigParser
import sys

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity

import log


class WaarLayer(YowInterfaceLayer):
    logger = log.init_logger(__name__)
    config_parser = SafeConfigParser()
    config_parser.read(os.path.join(sys.path[0], "waar.cfg"))

    block_file = config_parser.get("path", "blockfile")
    logger.info("[RESPONDER STARTED]")

    @ProtocolEntityCallback("message")
    def on_message(self, message):
        # send receipt otherwise we keep receiving the same message over and over
        if True:
            if not self.is_sender_blocked(message):
                self.logger.info("[MESSAGE RECEIVED] [%s] %s", message.getNotify(),
                                 message.getBody())
                self.send_receipt(message)
                self.send_response(message)
            else:
                self.logger.info("[MESSAGE RECEIVED] [IS BLOCKED] [%s] %s", message.getNotify(),
                                 message.getBody())
                self.send_receipt(message)

    def send_response(self, recipient):
        # Enter your response here
        response = "Hello {0}, this is an automated response!".format(recipient.getNotify())
        outgoingMessageProtocolEntity = TextMessageProtocolEntity(response, to=recipient.getFrom())
        self.toLower(outgoingMessageProtocolEntity)
        self.logger.info("[MESSAGE SENT] [%s] %s", recipient.getNotify(), response)

    def send_receipt(self, recipient):
        receipt = OutgoingReceiptProtocolEntity(recipient.getId(), recipient.getFrom())
        self.toLower(receipt)

    @ProtocolEntityCallback("receipt")
    def on_receipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery")
        self.toLower(ack)

    # checks if the auto response has already been sent to a group or a single contact
    def is_sender_blocked(self, message):
        block_list = self.get_block_list()
        is_blocked = False
        # check if the message comes from a group
        if "@g.us" in message.getFrom():
            sender = message.getFrom().split("-")[1]
        else:
            sender = message.getFrom()

        if sender in block_list:
            is_blocked = True
            return is_blocked
        # add sender to the blocklist
        block_list.append(sender)
        with open(self.block_file, "w") as block_file:
            json.dump(block_list, block_file)
        self.logger.info("[ADDED TO BLOCKLIST] %s", sender)
        self.logger.info("[BLOCKLIST :] %s", block_list)

        return is_blocked

    def get_block_list(self):
        try:
            block_list = json.loads(open(self.block_file).read())
        except (IOError, ValueError):
            open(self.block_file, "w").close()
            block_list = []
        return block_list
