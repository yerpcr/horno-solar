import network
from machine import Timer,ADC, Pin
from umqtt.simple import MQTTClient
from time import sleep_ms
import ubinascii
dato =['a','b','c']
analogo = ADC(0)
TOPIC = "prueba"
led_interno = Pin(2,Pin.OUT)
transistor = Pin(14,Pin.OUT)
led_rojo = Pin(0,Pin.OUT)
led_blanco = Pin(12,Pin.OUT)

led_rojo.value(0)
transistor.value(1)
temp = Timer(-1)
led_interno.value(0)
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
	led_rojo.value(1)

conectar()
led_interno.value(1)
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
cliente = MQTTClient(client_id=CLIENT_ID, server=dato[2],keepalive=1)
cliente.set_callback(enviar) ##Define una funcion que se activa cada interaccion 
cliente.connect()
cliente.subscribe(TOPIC)
print("Connected to server %s, subscribed to topic: %s" % (dato[2], TOPIC))
print("Configurando temporizador")
temp.init(mode=Timer.PERIODIC,period=5000,callback=funcion)
print("Listo")
while (1):
	if (led_rojo.value()==1):
		try:
			transistor.value(0)
			sleep_ms(1)
			entrada = analogo.read()
			print(entrada)
			transistor.value(1)
			cliente.publish(topic=TOPIC,msg=str(entrada))
			led_rojo.value(0)
		except:
			led_blanco.value(1)
			cliente.connect()
			led_blanco.value(0)
