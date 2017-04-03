from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os, subprocess
from socket import *
from architecture import Serverp2p, Clientp2p
from threading import Thread, current_thread
import random
from form_dict import AddElem
import netifaces

class index(QDialog):
	def __init__(self, parent=None):
		super(index, self).__init__(parent)

		
		self.setWindowTitle("Peer")
		ip = netifaces.ifaddresses('wlan0')[2][0]['addr']
		self.qPort = QInputDialog.getText(self, 'Informe a porta', 'IP detectado como '+ip+'. \nTecle enter para confirmar ou informe o seu IP correto na rede:')
		print(self.qPort[0])
		if self.qPort[0] != '':
			ip = self.qPort[0]
		self.server = Serverp2p(ip)
		self.connect(self.server, SIGNAL("success(QString)"), self.success)
		self.connect(self.server, SIGNAL("fail()"), self.fail)
		self.server.start()
		# self.client = Clientp2p()
		# self.client.start()
		informe = QLabel("Servico rodando na porta "+ip)
		hbox = QHBoxLayout()
		hbox.addWidget(informe)
		label = QLabel("Procure por palavra: ")
		self.nome_lineEdit = QLineEdit("")
		self.search = QPushButton("Procurar")
		hbox1 = QHBoxLayout()
		hbox1.addWidget(label)
		hbox1.addWidget(self.nome_lineEdit)
		hbox1.addWidget(self.search)
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

		self.connect(self.search, SIGNAL("clicked()"), self.averiguar)
		self.connect(add_vizinho, SIGNAL("clicked()"), self.add_viz)
		self.connect(button_add_word, SIGNAL("clicked()"), self.add_word)
		self.connect(button_remove_all_word, SIGNAL("clicked()"), self.clear_list)


		self.setGeometry(300,100,700,430)

	def averiguar(self):
		try:
			sorteado = random.choice(self.lista_de_vizinhos)
			print("A rota a seguir eh: {}".format(sorteado))
			self.client = Clientp2p(self.nome_lineEdit.displayText(), self.qPort[0], sorteado)
			self.client.start()
		except Exception as e:
			self.client = Clientp2p(self.nome_lineEdit.displayText(), self.qPort[0], '')
			self.client.start()

	def add_viz(self):
		add = QInputDialog.getText(self, 'Adicionando IP vizinho', 'Adicione um IP valido:')
		self.lista_de_vizinhos.append(add[0])
		self.inforvizinhos.setText("Vizinhos proximos: " + str(self.lista_de_vizinhos))

	def success(self, significado):
		msg = QMessageBox.information(self, "Sucesso!",
											"Significado da palavra encontrado: "+significado,
											 QMessageBox.Close)
	def fail(self):
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
		

app = QApplication(sys.argv)
dlg = index()
dlg.exec_()