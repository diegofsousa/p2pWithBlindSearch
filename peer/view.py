from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os, subprocess
from socket import *
from architecture import Serverp2p, Clientp2p
from threading import Thread, current_thread
import random
from form_dict import AddElem
import netifaces
import time, sys
from timer_tll import TLL

class index(QDialog):
	def __init__(self, parent=None):
		super(index, self).__init__(parent)

		
		self.setWindowTitle("Peer")
		self.ip = netifaces.ifaddresses('wlan0')[2][0]['addr']
		self.qPort = QInputDialog.getText(self, 'Informe a porta', 'IP detectado como '+self.ip+'. \nTecle enter para confirmar ou informe o seu IP correto na rede:')
		print(self.qPort[0])
		if self.qPort[0] != '':
			self.ip = self.qPort[0]
		self.server = Serverp2p(self.ip)
		self.connect(self.server, SIGNAL("success(QString)"), self.success)
		self.connect(self.server, SIGNAL("fail()"), self.fail)
		self.connect(self.server, SIGNAL("forward(QString)"), self.forward_search)

		self.server.start()
		# self.client = Clientp2p()
		# self.client.start()
		informe = QLabel("Servico rodando na porta "+self.ip)
		hbox = QHBoxLayout()
		hbox.addWidget(informe)
		label = QLabel("Procure por palavra: ")
		self.nome_lineEdit = QLineEdit("")
		self.search = QPushButton("Procurar")
		self.tll = 5
		self.label_tll = QLabel("TLL: " + str(self.tll))
		hbox1 = QHBoxLayout()
		hbox1.addWidget(label)
		hbox1.addWidget(self.nome_lineEdit)
		hbox1.addWidget(self.search)
		hbox1.addWidget(self.label_tll)
		self.lista_de_palavras = []

		informedic = QLabel("Dicionario contido neste servico:")
		self.lista = QListWidget()
		for i in self.lista_de_palavras:
			item = QListWidgetItem("Palavra: "+i.split(':')[0]+" - Significado: "+i.split(':')[1])
			self.lista.addItem(item)

		button_add_word = QPushButton("Adicionar palavra ao dicionario")
		button_remove_all_word = QPushButton("Limpar dicionario")

		hbox2 = QHBoxLayout()
		hbox2.addWidget(button_add_word)
		hbox2.addWidget(button_remove_all_word)

		
		self.inforvizinhos = QLabel("Vizinhos proximos: " + str(self.lista_de_palavras))
		add_vizinho = QPushButton("Adicionar vizinho")

		vbox = QVBoxLayout()
		vbox.addWidget(informedic)
		vbox.addWidget(self.lista)
		vbox.addLayout(hbox2)
		vbox.addWidget(add_vizinho)
		vbox.addWidget(self.inforvizinhos)

		self.lista_de_vizinhos = []


		vbox1 = QVBoxLayout()
		vbox1.addLayout(hbox)
		vbox1.addLayout(hbox1)
		vbox1.addLayout(vbox)

		self.setLayout(vbox1)

		self.ttll = TLL()

		self.connect(self.ttll, SIGNAL("timeo()"), self.timer_func)
		self.connect(self.ttll, SIGNAL("timeover()"), self.time_over)

		self.connect(self.search, SIGNAL("clicked()"), self.averiguar)
		self.connect(add_vizinho, SIGNAL("clicked()"), self.add_viz)
		self.connect(button_add_word, SIGNAL("clicked()"), self.add_word)
		self.connect(button_remove_all_word, SIGNAL("clicked()"), self.clear_list)

		
		self.setGeometry(300,100,700,430)

	def averiguar(self):
		self.ttll.start()
		if len(self.lista_de_vizinhos) == 0:
			self.ttll.terminate()
			msg = QMessageBox.information(self, "Erro!",
											"Nao ha nenhum IP vizinho conectado.",
											 QMessageBox.Close)
		else:
			try:
				sorteado = random.choice(self.lista_de_vizinhos)
				print("A rota a seguir eh: {}".format(sorteado))
				self.client = Clientp2p(self.nome_lineEdit.displayText(), self.ip, sorteado)
				self.client.start()
			except Exception as e:
				self.client = Clientp2p(self.nome_lineEdit.displayText(), self.ip, '')
				self.client.start()

	def add_viz(self):
		add = QInputDialog.getText(self, 'Adicionando IP vizinho', 'Adicione um IP valido:')
		self.lista_de_vizinhos.append(add[0])
		self.inforvizinhos.setText("Vizinhos proximos: " + str(self.lista_de_vizinhos))

	def success(self, significado):
		self.tll = 5
		self.label_tll.setText("TLL: "+str(self.tll))
		msg = QMessageBox.information(self, "Sucesso!",
											"Significado da palavra encontrado: "+significado,
											 QMessageBox.Close)
	def fail(self):
		self.tll = 5
		self.label_tll.setText("TLL: "+str(self.tll))
		msg = QMessageBox.information(self, "Falha!",
											"Falha ao encontar significado da palavra:",
											 QMessageBox.Close)

	def add_word(self):
		# self.ex = AddElem()
		# self.ex.start()
		ex = AddElem(self)
		a = self.connect(ex, SIGNAL("reload(QString)"), self.reload)
		print(a)
		
		ex.setModal(True)
		ex.show()
		#print(self.lista_de_vizinhos)

	def reload(self, palavra):
		self.lista_de_palavras.append(palavra)
		item = QListWidgetItem("Palavra: "+palavra.split(':')[0]+" - Significado: "+palavra.split(':')[1])
		self.lista.addItem(item)
		self.server.add_di_lista(palavra)
		print("Listando ...")
		print(self.server.get_list_lista())

	def clear_list(self):
		self.lista.clear()

	def decrem_tll(self):
		timer = QTimer()		
		timer.start(1000)
		for i in range(0, 5):
			timer.timeout.connect(self.timer_func)
			timer.remainingTime()

	def timer_func(self):
		print("decrementando")
		self.tll -= 1
		self.label_tll.setText("TLL: "+str(self.tll))

	def time_over(self):
		self.tll = 5
		self.label_tll.setText("TLL: "+str(self.tll))
		msg = QMessageBox.information(self, "Falha!",
											"Tempo de espera por mensagem acabou.",
											 QMessageBox.Close)
		self.client.terminate()

	def forward_search(self, palavra):
		try:
			sorteado = random.choice(self.lista_de_vizinhos)
			print("A rota a seguir eh: {}".format(sorteado))
			self.client = Clientp2p(palavra.split('^')[0], palavra.split('^')[1], sorteado)
			self.client.start()
		except Exception as e:
			self.client = Clientp2p(self.nome_lineEdit.displayText(), self.ip, '')
			self.client.start()

			


app = QApplication(sys.argv)
dlg = index()
dlg.exec_()