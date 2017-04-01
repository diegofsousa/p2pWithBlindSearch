from PyQt4.QtCore import *
from PyQt4.QtGui import *
from socket import *
import time, _thread as thread



class Serverp2p(QThread):
	def __init__ (self, port):
		self.port = port
		QThread.__init__(self)

	def run(self):
		print(self.port)
		self.meuHost = '127.0.0.1'
		#self.minhaPort = int(self.port)
		self.sockobj = socket(AF_INET, SOCK_STREAM)
		self.sockobj.bind((self.meuHost, self.port))
		self.sockobj.listen(5)
		print("Server rodando em: " + self.meuHost + " - Porta: " + str(self.port))
		self.arquivo()
		self.neighbors()
		self.despacha()

	def get_dicionario(self):
		return self.le(self.arquivo())
	
	def arquivo(self):
		try:
			arq = open('files/dicionario'+str(self.port)+'.data', 'r')
		except Exception as e:
			arq = open('files/dicionario'+str(self.port)+'.data', 'a')
		return arq

	def neighbors(self):
		try:
			arq = open('files/vizinhos'+str(self.port)+'.data', 'r')
		except Exception as e:
			arq = open('files/vizinhos'+str(self.port)+'.data', 'a')
		return arq

	def get_neighbors(self):
		lista = []
		arquivo = self.neighbors()
		linha = arquivo.readline()
		while linha:
			lista.append(int(linha.replace("\n", "")))
			linha = arquivo.readline()
		return lista

	def le(self, arquivo):
		dicionario = {}
		linha = arquivo.readline()
		while linha:
			dicionario[linha.split(':')[0]] = linha.split(':')[1]
			linha = arquivo.readline()
		return dicionario

	def busca(self, data):
		arq = self.arquivo()
		try:
			return self.le(arq)[data]
		except Exception as e:
			return 'Nada foi encontrado'

	def lidaCliente(self, conexao):
		while True:
			data = conexao.recv(1024)
			if not data: break
			conexao.send(self.busca(data.decode()).encode())

	def despacha(self):
		while True:
			conexao, endereco = self.sockobj.accept()
			print('Server conectado por', endereco)
			thread.start_new_thread(self.lidaCliente, (conexao,))

class Clientp2p(QThread):
	def __init__ (self):
		QThread.__init__(self)

	def run(self):
		serverHost = 'localhost'
		serverPort = 5014

		sockobj = socket(AF_INET, SOCK_STREAM)
		sockobj.connect((serverHost, serverPort))

		linha = input("Informe a mensagem a ser buscada: ")

		sockobj.send(linha.encode())

		data = sockobj.recv(1024)
		print("Cliente recebeu: ", data)

		sockobj.close()
