#Sensori Magnetometro da trasferire tramite bluetooth
import board
import lsm9ds1
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
        periph.advertise(device_name="Sensor", services=[service])
    elif id == constants.EVT_GATTS_WRITE:
        # write to this Characteristic is to CCCD
        if int(data[0]) == 1:
            notif_enabled = True
        else:
            notif_enabled = False

# start off with LED(1) off
LED(1).off()

notif_enabled = False
#0x183B sensore service
uuid_sensor = UUID("0X183B")  # Sensor service
#Indirizzo per la lettura dei vari sensori
uuid_service = UUID("0x2A5D")  # Sensore characteristic
#uuid_PROVA=UUID("0X2A36")

service = Service(uuid_service)
sensor_props = Characteristic.PROP_READ|Characteristic.PROP_NOTIFY
sensor_attrs = Characteristic.ATTR_CCCD
sensor_char = Characteristic(uuid_sensor, props=sensor_props, attrs=sensor_attrs)
service.addCharacteristic(sensor_char)

periph = Peripheral()
periph.addService(service)
periph.setConnectionHandler(event_handler)
periph.advertise(device_name="Magnetometro", services=[service])

bus = I2C(1, scl=Pin(15), sda=Pin(14))
lsm = lsm9ds1.LSM9DS1(bus)

while (True):
    if notif_enabled:
       #Inizializzazione e visualizzazione dei dati del magnetometro
         magnetometro_x, magnetometro_y, magnetometro_z = lsm.read_magnet()

        #Inzializzazione asse x magnetometro
         magne_x=('assex:{:>8.3f}'.format(magnetometro_x))
         sensor_char.write(magne_x)
         print(magne_x)
         time.sleep_ms(100)

         #Inzializzazione asse y magnetometro
         magne_y=('assey:{:>8.3f}'.format(magnetometro_y))
         sensor_char.write(magne_y)
         print(magne_y)
         time.sleep_ms(100)

         #Inzializzazione asse z magnetometro
         magne_z=('assez:{:>8.3f}'.format(magnetometro_z))
         sensor_char.write(magne_z)
         print(magne_z)


         time.sleep_ms(100)


    time.sleep_ms(100)
