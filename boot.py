
import gc
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
from machine import Pin
from time import sleep
esp.osdebug(None)
gc.collect()

led = Pin(2, Pin.OUT, value=1)
pump = Pin(13, Pin.OUT, value=1)

# ssid = 'SPWN_H36_E5B8E2'
# password = '9amfeyrjry66eh4'
# mqtt_server = '192.168.100.100'

ssid = '3104145E'
password = '0850023821'
mqtt_server = '192.168.43.43'

# EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'home/pumper_1/control'
topic_pub = b'home/pumper_1/status'
station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)
print('Connecting..........')
while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())
led.value(0)
state = b'off'

