__author__	  = "Christopher Piekarski"
__email__	   = "polo1065@gmail.com"
__copyright__= " Copyright, 2011"
__version__	 = "1.0.0"

""" This entire file is simply a set of examples. The most basic is to
simply create a custom server by inheriting threadedServer.ThreadedServer
as shown below in MyServer.
"""

import threadedServer
import jsonSocket
import logging

logger = logging.getLogger("jsonSocket.customServer")

class MyServer(threadedServer.ThreadedServer):
	""" This is a basic example of a custom ThreadedServer. """
	def __init__(self):
		super(MyServer, self).__init__()
		self.timeout = 2.0
		logger.warning("MyServer class in customServer is for example purposes only.")
	
	def _process_message(self, obj):
		""" virtual method """
		if obj != '':
			if obj['message'] == "new connection":
				logger.info("new connection.")
			   

class MyFactoryThread(threadedServer.FactoryServerThread):
	""" This is an example factory thread, which the server factory will
		instantiate for each new connection.
	"""
	def __init__(self):
		super(MyFactoryThread, self).__init__()
		self.timeout = 2.0
	
	def _process_message(self, obj):
		""" virtual method - Implementer must define protocol """
		if obj != '':
			if obj['message'] == "new connection":
				logger.info("new connection.")
			else:
				logger.info(obj)
	
if __name__ == "__main__":
	import time
	server = threadedServer.FactoryServer(MyFactoryThread)
	server.timeout = 2.0
	server.start()
	
	time.sleep(1)
	cPids = []
	for i in range(10):
		client = jsonSocket.JsonClient()
		cPids.append(client)
		client.connect()
		client.sendObj({"message": "new connection"})
		client.sendObj({"message": i })
	
	time.sleep(2)
	
	for c in cPids:
		c.close()
	server.stop()
	server.join()