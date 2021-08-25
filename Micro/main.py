from machine import network
print ("Leer datos")
def conectar ():
	archivo = open('wifi.txt','r')
	dato  = archivo.read().split(',')
	archivo.close()
	sta_if = network.WLAN(network.STA_IF)
	if not sta_if.isconnected():
		print('connecting to network...')
		sta_if.active(True)
		sta_if.connect(dato[0], dato[1])
		while not sta_if.isconnected():
			pass
		print('network config:', sta_if.ifconfig())

conectar()