from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
import threading
import logging
import sys
import time
from yowsup.layers.protocol_receipts.protocolentities  import IncomingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import IncomingAckProtocolEntity, OutgoingAckProtocolEntity

logger = logging.getLogger(__name__)

class SendLayer(YowInterfaceLayer):

    #This message is going to be replaced by the @param message in YowsupSendStack construction
    #i.e. list of (jid, message) tuples
    PROP_MESSAGES = "org.openwhatsapp.yowsup.prop.sendclient.queue"


    def __init__(self):
        super(SendLayer, self).__init__()
        self.ackQueue = []
        self.lock = threading.Condition()

    #call back function when there is a successful connection to whatsapp server
    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        self.lock.acquire()
        
        for target in self.getProp(self.__class__.PROP_MESSAGES, []):
            #getProp() is trying to retreive the list of (jid, message) tuples, if none exist, use the default []
            print "@@@@@@", target
            print "mmmmm", "Spiniiiiiii"
            phone, message = target
            #phone = target
            #message = "Spiniiiii"
            #receipt = OutgoingReceiptProtocolEntity()
            if '@' in phone:
                messageEntity = TextMessageProtocolEntity(message, to = phone)
            elif '-' in phone:
                messageEntity = TextMessageProtocolEntity(message, to = "%s@g.us" % phone)
            else:
                print "qqqqqq"
                messageEntity = TextMessageProtocolEntity(message, to = "%s@s.whatsapp.net" % phone)
            receipt = IncomingReceiptProtocolEntity(messageEntity.getId(), phone, 'read', messageEntity.getParticipant())
            entity = IncomingAckProtocolEntity(receipt.getId(), 'receipt', phone, int(time.time()))
            print entity.getId()
            print "-->>", messageEntity.getId(), messageEntity.getFrom(), messageEntity.getParticipant()
            print "###", receipt.getId(), "type", receipt.getType()
            #append the id of message to ackQueue list
            #which the id of message will be deleted when ack is received.
            self.ackQueue.append(messageEntity.getId())
            self.toLower(messageEntity)
           # self.toLower(receipt)
        self.lock.release()
        print "lock released"


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print "aaaaa", entity.getId()
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery")
        self.toLower(ack)

    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        self.lock.acquire()
        #if the id match the id in ackQueue, then pop the id of the message out
        if entity.getId() in self.ackQueue:
            print "Id received", entity.getId()
            #print entity.type()
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))
        if not len(self.ackQueue):
            #self.lock.release()
            print "message sent"
            logger.info("Message sent")
            #raise KeyboardInterrupt()
        self.lock.release()

    #@ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print "inside onReceipt"
        ack = IncomingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        
        self.toLower(ack)
