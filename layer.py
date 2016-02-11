from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
import time


class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over

        if True:
            #receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'delivered', messageProtocolEntity.getParticipant())
            print messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), messageProtocolEntity.getParticipant()
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                "Hello World",#messageProtocolEntity.getBody() 
                to = messageProtocolEntity.getFrom())
            time.sleep(10)
            self.toLower(outgoingMessageProtocolEntity)
            #time.sleep(10)
            #self.toLower(receipt)
           #self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print "Id-->", entity.getId(), "Type-->", entity.getType(), "From-->", entity.getFrom()
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)
