from PyQt4.QtCore import *
from PyQt4.QtGui import *
from socket import *
import time, _thread as thread
from response import devolve


class Serverp2p(QThread):
	def __init__ (self, meuHost):
		self.meuHost = meuHost
		QThread.__init__(self)

	def run(self):
		#self.minhaPort = int(self.port)
		self.sockobj = socket(AF_INET, SOCK_STREAM)
		self.sockobj.bind((self.meuHost, 5000))
		self.sockobj.listen(5)
		print("Server rodando em: " + self.meuHost + " - Porta: " + str(5000))
		self.arquivo()
		self.neighbors()
		self.despacha()

	def get_dicionario(self):
		return self.le(self.arquivo())
	
	def arquivo(self):
		try:
			arq = open('files/dicionario.data', 'r')
		except Exception as e:
			arq = open('files/dicionario.data', 'a')
		return arq

	def neighbors(self):
		try:
			arq = open('files/vizinhos.data', 'r')
		except Exception as e:
			arq = open('files/vizinhos.data', 'a')
		return arq

	def get_neighbors(self):
		lista = []
		arquivo = self.neighbors()
		try:
			linha = arquivo.readline()
			while linha:
				lista.append(linha.replace("\n", ""))
				linha = arquivo.readline()
			return lista
		except Exception as e:
			print('Erro de achar vizinho: '+e)
			return False		

	def le(self, arquivo):
		dicionario = {}
		linha = arquivo.readline()
		while linha:
			dicionario[linha.split(':')[0]] = linha.split(':')[1]
			linha = arquivo.readline()
		return dicionario


	def busca(self, data):
		if(data.split('^')[0] == 'r'):
			print("Achou a palavra: "+data.split('^')[1])
		elif(data.split('^')[0] == 'e'):
			print("Não achamos a peca certa "+data.split('^')[1])
		else:
			print("Chegou na função de busca")
			#print(data)
			#print(data.split('^')[1] + " esta buscando por " + data.split('^')[0] + ' em ' + str(self.get_dicionario()))
			arq = self.arquivo()
			print(data.split('^')[0])
			try:
				significado = self.le(arq)[data.split('^')[0]]
				if significado:					
					thread.start_new_thread(devolve, (data.split('^')[1], significado))
			except Exception as e:
				print('Erro de busca')
				#raise e
				return 'Nada foi encontrado'

	def lidaCliente(self, conexao):
		while True:
			data = conexao.recv(1024)
			if not data: break
			self.busca(data.decode())

	def despacha(self):
		while True:
			conexao, endereco = self.sockobj.accept()
			print('Server conectado por', endereco)
			thread.start_new_thread(self.lidaCliente, (conexao,))

class Clientp2p(QThread):
	def __init__ (self, word, fromm, ipsearch):
		self.word = word
		self.fromm = fromm
		self.ipsearch = ipsearch
		QThread.__init__(self)

	def run(self):
		serverHost = self.ipsearch
		if self.ipsearch == '':
			sockobj = socket(AF_INET, SOCK_STREAM)
			sockobj.connect((self.ipsearch, 5000))
			wordok = 'e^'+str(self.word)

			#linha = input("Informe a mensagem a ser buscada: ")

			sockobj.send(wordok.encode())

			data = sockobj.recv(1024)
			#print("Cliente recebeu: ", data)

			sockobj.close()
		else:
			sockobj = socket(AF_INET, SOCK_STREAM)
			sockobj.connect((serverHost, 5000))
			wordok = str(self.word)+'^'+str(self.fromm)

			#linha = input("Informe a mensagem a ser buscada: ")

			sockobj.send(wordok.encode())
			data = sockobj.recv(1024)
			sockobj.close()
