from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os, subprocess
from socket import *
from architecture import Serverp2p, Clientp2p
from threading import Thread, current_thread
import random

class index(QDialog):
	def __init__(self, parent=None):
		super(index, self).__init__(parent)
		
		self.setWindowTitle("Peer")
		self.qPort = QInputDialog.getText(self, 'Informe a porta', 'Antes se começar, informe o seu IP na rede:')
		print(self.qPort[0])
		self.server = Serverp2p(self.qPort[0])
		self.server.start()
		# self.client = Clientp2p()
		# self.client.start()
		informe = QLabel("Servico rodando na porta "+str(self.qPort[0]))
		hbox = QHBoxLayout()
		hbox.addWidget(informe)
		label = QLabel("Procure por palavra: ")
		self.nome_lineEdit = QLineEdit("")
		self.search = QPushButton("Procurar")
		hbox1 = QHBoxLayout()
		hbox1.addWidget(label)
		hbox1.addWidget(self.nome_lineEdit)
		hbox1.addWidget(self.search)

		informedic = QLabel("Dicionario contido neste servico:")
		lista = QListWidget()
		for i in list(self.server.get_dicionario().items()):
			item = QListWidgetItem("Palavra: "+i[0]+" - Significado: "+i[1].replace("\n",""))
			lista.addItem(item)

		inforvizinhos = QLabel("Vizinhos proximos: " + str(self.server.get_neighbors()))

		vbox = QVBoxLayout()
		vbox.addWidget(informedic)
		vbox.addWidget(lista)
		vbox.addWidget(inforvizinhos)


		vbox1 = QVBoxLayout()
		vbox1.addLayout(hbox)
		vbox1.addLayout(hbox1)
		vbox1.addLayout(vbox)
		print(self.server.get_dicionario())

		self.setLayout(vbox1)

		self.connect(self.search, SIGNAL("clicked()"), self.averiguar)

		self.setGeometry(300,100,700,430)

	def averiguar(self):
		try:
			sorteado = random.choice(self.server.get_neighbors())
			print("A rota a seguir eh: {}".format(sorteado))
			self.client = Clientp2p(self.nome_lineEdit.displayText(), self.qPort[0], sorteado)
			self.client.start()
		except Exception as e:
			self.client = Clientp2p(self.nome_lineEdit.displayText(), self.qPort[0], '')
			self.client.start()
		

app = QApplication(sys.argv)
dlg = index()
dlg.exec_()