from PyQt4.QtCore import *
from PyQt4.QtGui import *
from socket import *
import time, _thread as thread
from response import devolve
import time, sys


class TLL(QThread):
	def __init__ (self):
		QThread.__init__(self)

	def run(self):
		for i in range(0,5):
			self.decr()
			time.sleep(1)
		self.emit(SIGNAL("timeover()"))
		# timer = QTimer()
		# timer.start(1000)
		# self.connect(timer, SIGNAL("timeout()"), self.decr)
		

	def decr(self):
		print("decre")
		self.emit(SIGNAL("timeo()"))