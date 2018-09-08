# -*- coding: utf-8 -*-

from twisted.internet.protocol import Protocol,ClientFactory
from  sys import stdout


class Echo(Protocol):
	def __init__(self):
		self.connected = False

	def connectionMade(self):
		self.connected =True
	# def connectionLost(self,reason):
	# 	self.connected =False
	def dataReceived(self,data):
		print data.decode('utf8')
class EchoClientFactory(ClientFactory):
	def __init__(self):
		self.protocol = None

	def startedConnecting(self,connector):
		print 'Started to connect'

	def buildProtocol(self,connector):
		print "Connect"
		self.protocol = Echo()
		return self.protocol

	def clientConnectionLost(self,connector,reason):
		print 'Lost connection. Reason:', reason

	def clientConnectionFailed(self,connector,reason):
		print 'Connection failed. Reason:', reason


from twisted.internet import reactor
import threading
import fileinput
import time
import datetime
import sys

bStop = False
def routine(factory):
	while not bStop:
		if factory.protocol and factory.protocol.connected:
			factory.protocol.transport.write("hello, I'm %s %s" % (sys.argv[1],datetime.datetime.now(),))
	time.sleep(5)

host = "127.0.0.1"
port = 8007
factory = EchoClientFactory()
reactor.connectTCP(host,port,factory)
threading.Thread(target=routine,args=(factory,)).start()
reactor.run()
bStop = True