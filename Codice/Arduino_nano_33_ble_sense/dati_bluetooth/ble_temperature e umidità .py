# HTS221 + BLE example.

import time
import hts221
from board import LED
from machine import Pin, I2C
from ubluepy import Service, Characteristic, UUID, Peripheral, constants

def event_handler(id, handle, data):
    global periph, service, notif_enabled

    if id == constants.EVT_GAP_CONNECTED:
        # indicated 'connected'
        LED(1).on()
    elif id == constants.EVT_GAP_DISCONNECTED:
        # indicate 'disconnected'
        LED(1).off()
        # restart advertisment
        periph.advertise(device_name="Temperature Sensor", services=[service])
    elif id == constants.EVT_GATTS_WRITE:
        # write to this Characteristic is to CCCD
        if int(data[0]) == 1:
            notif_enabled = True
        else:
            notif_enabled = True

# start off with LED(1) off
LED(1).off()

notif_enabled = False
uuid_service = UUID("0x181A")  # Environmental Sensing service
uuid_temp    = UUID("0x2A6E")  # Temperature characteristic
uuid_hum    = UUID("0x2A6F")  # Temperature characteristic


service = Service(uuid_service)
temp_props = Characteristic.PROP_READ|Characteristic.PROP_NOTIFY
temp_attrs = Characteristic.ATTR_CCCD
#hum_props = Characteristic.PROP_READ|Characteristic.PROP_NOTIFY
#Hum_attrs = Characteristic.ATTR_CCCD
temp_char = Characteristic(uuid_temp, props=temp_props, attrs=temp_attrs)
hum_char = Characteristic(uuid_hum, props=temp_props, attrs=temp_attrs)
service.addCharacteristic(temp_char)
service.addCharacteristic(hum_char)

periph = Peripheral()
periph.addService(service)
periph.setConnectionHandler(event_handler)
periph.advertise(device_name="Temperatura e Umidità", services=[service])

bus = I2C(1, scl=Pin(15), sda=Pin(14))
hts_temp = hts221.HTS221(bus)
hts_hum=hts221.HTS221(bus)

while (True):
    if notif_enabled:
    #Da far andare uno alla volta altrimenti errore con la notifica
         temp = int(hts_temp.temperature()*100)#Con hts
         temp_char.write(bytearray([temp & 0xFF, temp >> 8]))
         #time.sleep_ms(100)
         #hum =int(hts_hum.humidity()*100)
        # hum_char.write(bytearray([hum & 0xFF, hum >> 8]))
   # time.sleep_ms(100)

