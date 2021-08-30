#!/usr/bin/python
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
import paho.mqtt.client as mqtt
broker = "192.168.0.22"
equipo = "Dell"
tema = "prueba"
class MyWidget(QtWidgets.QWidget): #Crea la aplicacion con base a la ventana inicial
    def __init__(self):
        super().__init__()
        self.text_r = QtWidgets.QLabel("Resistencia: 1.1ohms",
                                     alignment=QtCore.Qt.AlignCenter)
        self.text_v = QtWidgets.QLabel("Voltaje",
                                     alignment=QtCore.Qt.AlignCenter)
        self.text_i = QtWidgets.QLabel("Corriente",
                                     alignment=QtCore.Qt.AlignCenter)
        self.text_p = QtWidgets.QLabel("Potencia",
                                     alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text_r)
        self.layout.addWidget(self.text_v)
        self.layout.addWidget(self.text_i)
        self.layout.addWidget(self.text_p)

    def actualizacion(self,client, userdata, message):
    	dato = str(message.payload.decode("utf-8"))
    	valor_v = float(dato)/1.023
    	valor_i = valor_v/1.1
    	valor_p = valor_v*valor_i
    	print("Dato: ",dato)
    	self.text_v.setText( "Volatje: {0:.3f} mV".format(valor_v))
    	self.text_i.setText( "Corriente: {0:.3f} mA".format(valor_i))
    	self.text_p.setText( "Potencia: {0:.3f} uP".format(valor_p))


if __name__ == "__main__":
	print("Creacion del cliente Mqtt")
	cliente = mqtt.Client(equipo)
	aplicacion = QtWidgets.QApplication([])
	principal = MyWidget()
	cliente.on_message = principal.actualizacion
	print("Conectando con el broker")
	cliente.connect(broker)
	print("Subscripcion a:", tema)
	cliente.subscribe(tema)
	cliente.loop_start()
	principal.resize(200, 300)
	principal.show()

aplicacion.exec()