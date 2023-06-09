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
        #Connessione bluetooth dell'arduino
        LED(1).on()
    elif id == constants.EVT_GAP_DISCONNECTED:
        #Disconnessione bluetooth
        LED(1).off()

        periph.advertise(device_name="Sensor", services=[service])
    elif id == constants.EVT_GATTS_WRITE:

        if int(data[0]) == 1:
            notif_enabled = True
        else:
            notif_enabled = False

# Inizializzo con led disattivato
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
periph.advertise(device_name="Accelerometro", services=[service])

bus = I2C(1, scl=Pin(15), sda=Pin(14))
lsm = lsm9ds1.LSM9DS1(bus)

while (True):
    if notif_enabled:
       #Inizializzazione e visualizzazione dei dati dell'accelerometro
        accel_x, accel_y, accel_z = lsm.read_accel()
        #valori moltiplicati*1000
        #temp=float(accel_x*1000)
        acc_x=('assex:{:>8.3f}'.format(accel_x))
        time.sleep_ms(100)
        acc_y=('assey:{:>8.3f}'.format(accel_y))
        time.sleep_ms(100)
        acc_z=('assez:{:>8.3f}'.format(accel_z))
        time.sleep_ms(100)
       # print(temp)
        print(accel_x)
        #print("Asse y accelerometro:",accel_y)
        #print("Asse z accelerometro:",accel_z)

        sensor_char.write(acc_x)
        sensor_char.write(acc_y)
        sensor_char.write(acc_z)
    time.sleep_ms(100)
