# -*- coding: utf-8 -*-

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
import log
import json


class WaarLayer(YowInterfaceLayer):
    BLOCK_FILE = "blocklist.json"
    LOGGER = log.init_logger('root')
    LOGGER.info("[RESPONDER STARTED]")

    @ProtocolEntityCallback("message")
    def onMessage(self, message):
        if True:
            if not self.isSenderBlocked(message):
                self.LOGGER.info(
                    "[MESSAGE RECEIVED] [{0}] {1}".format(message.getNotify(), message.getBody()))
                self.sendReceipt(message)
                self.sendResponse(message)
            else:
                self.LOGGER.info("[MESSAGE RECEIVED] [IS BLOCKED] [{0}] {1}".format(message.getNotify(),
                                                                                    message.getBody()))
                self.sendReceipt(message)

    def sendResponse(self, recipient):
        response = self.writeResponseMessageBody(recipient.getNotify())
        outgoingMessageProtocolEntity = TextMessageProtocolEntity(response, to=recipient.getFrom())
        self.toLower(outgoingMessageProtocolEntity)
        self.LOGGER.info(
            "[MESSAGE SENT] [{0}] {1}".format(recipient.getNotify(), response))

    def sendReceipt(self, recipient):
        receipt = OutgoingReceiptProtocolEntity(recipient.getId(), recipient.getFrom())
        self.toLower(receipt)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery")
        self.toLower(ack)

    def writeResponseMessageBody(self, name):
        response = "ENTER YOUR RESPONSE HERE!"
        return response


    # checks if the auto response has already been sent to a group or a single contact
    def isSenderBlocked(self, message):
        blocklist = self.init_block_list()
        isBlocked = False
        # check if the message comes from a group
        if "@g.us" in message.getFrom():
            sender = message.getFrom().split("-")[1]
        else:
            sender = message.getFrom()

        if sender in blocklist:
            isBlocked = True
            return isBlocked
        # add sender to the blocklist
        blocklist.append(sender)
        with open(self.BLOCK_FILE, "w") as f:
            json.dump(blocklist, f)
        self.LOGGER.info("[ADDED TO BLOCKLIST] {0}".format(sender))
        self.LOGGER.info("[BLOCKLIST :] {0}".format(blocklist))

        return isBlocked

    def init_block_list(self):
        try:
            blocklist = json.loads(open(self.BLOCK_FILE).read())
        except (IOError, ValueError):
            open(self.BLOCK_FILE, "w").close()
            blocklist = []
        return blocklist