from sendrun import YowsupSendStack
import json


CREDENTIALS = ("919560161879", "1hv9RPb8q+mVhPGHd9YhudJpmOs=") # replace with your phone and password

#unSender = YowsupSendStack(CREDENTIALS, (("918142202086","First message"),("918142202086", "Second Message") ))

#unSender.start() 

class HandleQueue:
    def sendMessage(self, message):
        message = self.parseAndFormatMessage(message) #message contains list of tuples with user number and message mapping
        sender = YowsupSendStack(CREDENTIALS, message)
        sender.start()
    
    def parseAndFormatMessage(self, message):
        parse_json = json.loads(message)
        message = ((parse_json['mobileNumber'], parse_json['messageBody']),)
        return message
        


