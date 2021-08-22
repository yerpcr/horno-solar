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

        self.text = QtWidgets.QLabel("Dato del sensor",
                                     alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)

    def actualizacion(self,client, userdata, message):
    	dato = str(message.payload.decode("utf-8"))
    	print("Dato: ",dato)
    	self.text.setText(dato)


if __name__ == "__main__":
	print("Creacion del cliente Mqtt")
	cliente = mqtt.Client(equipo)
	
	aplicacion = QtWidgets.QApplication([])
	principal = MyWidget()
	cliente.on_message = principal.actualizacion
	print("Conectando con el broker")
	cliente.connect(broker)
	cliente.loop_start()
	print("Subscripcion a:", tema)
	cliente.subscribe(tema)
	principal.resize(200, 300)
	principal.show()
	sys.exit(aplicacion.exec())