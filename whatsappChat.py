from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import IncomingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
import time

class ChatLayer(YowInterfaceLayer):
    
    PROP_MESSAGES = "org.openwhatsapp.yowsup.prop.sendclient.queue"

    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        for target in self.getProp(self.__class__.PROP_MESSAGES, []):
            phone, message = target
            messageEntity = TextMessageProtocolEntity(message, to=phone)
            receipt = IncomingReceiptProtocolEntity(messageEntity.getId(), phone, int(time.time()))
            self.toLower(messageEntity)
            print "Testing"
            self.toLower(receipt)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print "Inside receipt"
        self.toLower(entity.ack())

    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        self.lower(entity.ack())
