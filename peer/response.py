import time, _thread as thread
from socket import *

def devolve(ip, word):
	print(word)
	serverHost = ip
	serverPort = 5000

	sockobj = socket(AF_INET, SOCK_STREAM)
	sockobj.connect((serverHost, serverPort))
	word = "r^"+word

	#linha = input("Informe a mensagem a ser buscada: ")

	sockobj.send(word.encode())

	data = sockobj.recv(1024)
	#print("Cliente recebeu: ", data)

	sockobj.close()

# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# from socket import *

# class Responsep2p(QThread):
# 	def __init__ (self, ip, word):
# 		self.ip = ip
# 		self.word = word
# 		QThread.__init__(self)

# 	def run(self):
# 		print(self.word)
# 		# serverHost = self.ip
# 		# serverPort = 5000

# 		# sockobj = socket(AF_INET, SOCK_STREAM)
# 		# sockobj.connect((serverHost, serverPort))

# 		# #linha = input("Informe a mensagem a ser buscada: ")

# 		# sockobj.send(self.word.encode())

# 		# data = sockobj.recv(1024)
# 		# #print("Cliente recebeu: ", data)

# 		# sockobj.close()