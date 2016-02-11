from receiveMessageQueue import ReceivingMessage
from run import AcceptReceipt
thread1 = ReceivingMessage(1, "ReceiveMessage", "/queue/best")
thread2 = AcceptReceipt(2, "AcceptReceipt")
thread1.start()
thread2.start()
