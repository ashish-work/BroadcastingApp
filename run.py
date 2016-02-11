
from layer import EchoLayer
from yowsup.layers                             import YowParallelLayer
from yowsup.layers.auth                        import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.stacks import YowStack
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS
from yowsup.layers.axolotl                     import YowAxolotlLayer
from yowsup import env
import threading


CREDENTIALS = ("919560161879", "1hv9RPb8q+mVhPGHd9YhudJpmOs=") # replace with your phone and password

class AcceptReceipt(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    
    def run(self):
        layers = (
            EchoLayer,
            YowParallelLayer([YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer]),YowAxolotlLayer
            ) + YOWSUP_CORE_LAYERS

        stack = YowStack(layers)
        stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)         #setting credentials
        stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])    #whatsapp server address
        stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)              
        stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())          #info about us as WhatsApp client

        stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #sending the connect signal

        stack.loop() #this is the program mainloop      



thread = AcceptReceipt(1, "catchReceipt")
thread.start()
