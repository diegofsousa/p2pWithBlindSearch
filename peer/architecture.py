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
		self.neighbors = []
		self.dicionario_dict = {}
		self.sockobj = socket(AF_INET, SOCK_STREAM)
		self.sockobj.bind((self.meuHost, 5000))
		self.sockobj.listen(5)
		self.despacha()
		print("Server rodando em: " + self.meuHost + " - Porta: " + str(5000))


	def busca(self, data):
		if(data.split('^')[0] == 'r'):
			print("Achou a palavra: "+data.split('^')[1])
			self.emit(SIGNAL("success(QString)"), data.split('^')[1])
		elif(data.split('^')[0] == 'e'):
			print("Não achamos a peca certa "+data.split('^')[1])
			self.emit(SIGNAL("fail()"))
		else:
			print("Chegou na função de busca")
			#print(data)
			#print(data.split('^')[1] + " esta buscando por " + data.split('^')[0] + ' em ' + str(self.get_dicionario()))
			#arq = self.arquivo()
			print(data.split('^')[0])
			try:
				significado = self.dicionario_dict[data.split('^')[0]]
				#significado = self.le(arq)[data.split('^')[0]]
				if significado:					
					thread.start_new_thread(devolve, (data.split('^')[1], significado))
			except Exception as e:
				print('Erro de busca')
				self.emit(SIGNAL("forward(QString)"), data)				
				#raise e
				return 'Nada foi encontrado'

	def lidaCliente(self, conexao):
		while True:
			data = conexao.recv(1024)
			if not data: break
			conexao.send(b'Eco=> ')
			self.busca(data.decode())

	def despacha(self):
		while True:
			conexao, endereco = self.sockobj.accept()
			print('Server conectado por', endereco)
			thread.start_new_thread(self.lidaCliente, (conexao,))

	def add_di_lista(self, palavra):
		print(palavra)
		self.dicionario_dict[palavra.split(":")[0]] = palavra.split(":")[1]

	def get_list_lista(self):
		return self.dicionario_dict

class Clientp2p(QThread):
	def __init__ (self, word, fromm, ipsearch):
		self.word = word
		self.fromm = fromm
		self.ipsearch = ipsearch
		QThread.__init__(self)

	def run(self):		
		serverHost = self.ipsearch
		if self.ipsearch == '':
			print("Tentando enviar requisicao a "+ self.ipsearch)
			sockobj = socket(AF_INET, SOCK_STREAM)
			sockobj.connect((serverHost, 5000))
			wordok = 'e^'+str(self.word)

			#linha = input("Informe a mensagem a ser buscada: ")

			sockobj.send(wordok.encode())

			data = sockobj.recv(1024)
			print("Cliente recebeu: ", data)

			sockobj.close()
		else:
			print("Tentando enviar resposta a "+ self.ipsearch)
			sockobj = socket(AF_INET, SOCK_STREAM)
			sockobj.connect((serverHost, 5000))
			wordok = str(self.word)+'^'+str(self.fromm)

			#linha = input("Informe a mensagem a ser buscada: ")

			sockobj.send(wordok.encode())
			data = sockobj.recv(1024)
			print("Cliente recebeu: ", data)
			sockobj.close()
