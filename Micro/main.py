import network
from machine import Timer,ADC, Pin
from umqtt.simple import MQTTClient
import ubinascii
dato =['a','b','c']
analogo = ADC(0)
TOPIC = "prueba"
led = Pin(2,Pin.OUT)
temp = Timer(-1)
bandera=0
led.value(1)
def conectar ():
	global dato
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

def enviar():
	pass

def funcion(t):
	led.off()

conectar()
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
cliente = MQTTClient(CLIENT_ID, dato[2])
cliente.set_callback(enviar) ##Define una funcion que se activa cada interaccion 
cliente.connect()
cliente.subscribe(TOPIC)
print("Connected to server %s, subscribed to topic: %s" % (dato[2], TOPIC))
print("Configurando temporizador")
temp.init(mode=Timer.PERIODIC,period=2000,callback=funcion)
print("Listo")
try:
	while 1:
		# micropython.mem_info()
		if (led.value()==0):
			entrada = analogo.read()
			print(entrada)
			cliente.publish(topic=TOPIC,msg=str(entrada))
			bandera = 0;
			led.on()
finally:
	cliente.disconnect()