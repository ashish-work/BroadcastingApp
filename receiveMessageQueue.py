import time
import sys
import os
import stomp
from testsendclient import HandleQueue
import threading

class ReceivingMessage(threading.Thread):
    def __init__(self, threadID, name, queue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.queue = queue

    def run(self):
        user = os.getenv("ACTIVEMQ_USER") or "admin"
        password = os.getenv("ACTIVEMQ_PASSWORD") or "password"
        host = os.getenv("ACTIVEMQ_HOST") or "localhost"
        port = os.getenv("ACTIVEMQ_PORT") or 61613
        destination = self.queue
        destination = destination[0]
        print "user",user, "password", password,  "host", host, "port", port
        conn = stomp.Connection(host_and_ports = [(host, port)])
        conn.set_listener('', MyListener(conn))
        conn.start()
        conn.connect(login=user,passcode=password)
        conn.subscribe(destination=destination,id = 1,  ack='auto')
        #print ' '.join(sys.argv[1:])
        #conn.send(body=' '.join(sys.argv[1:]), destination='/queue/TestYowsup')
        print("Waiting for messages...")
        while 1:
            time.sleep(10)

class MyListener(object):

  def __init__(self, conn):
    self.conn = conn
    self.count = 0
    self.start = time.time()

  def on_error(self, headers, message):
    print('received an error %s' % message)

  def on_message(self, headers, message):
    print "QQQQQQQQ", message
    try:
        whatsApp = HandleQueue()
        whatsApp.sendMessage(message)
    except KeyboardInterrupt:
        print "Message delivered"
    diff = time.time() - self.start
    print self
    print("Received %s in %f seconds" % (self.count, diff))
    if message == "SHUTDOWN":

      diff = time.time() - self.start
      print("Received %s in %f seconds" % (self.count, diff))
      conn.disconnect()
      sys.exit(0) 
          
    else:
      if self.count==0:
        self.start = time.time()
        
      self.count += 1
      if self.count % 1000 == 0:
         print("Received %s messages." % self.count)

