import board
import lsm9ds1
import time
from machine import Pin, I2C

#Impostazione dei comandi I2C
bus = I2C(1, scl=Pin(15), sda=Pin(14))
lsm = lsm9ds1.LSM9DS1(bus)

while (True):
    #Inizializzazione e visualizzazione dei dati dell'accelerometro
    accel_x, accel_y, accel_z = lsm.read_accel()

    print("Asse x accelerometro:",accel_x)
    print("Asse y accelerometro:",accel_y)
    print("Asse z accelerometro:",accel_z)

    time.sleep_ms(500)

    #Inizializzazione e visualizzazione dei vari dati dell'accelerometro
    mag_x, mag_y, mag_z = lsm.read_magnet()

    print("Asse x magnetometro:",mag_x)
    print("Asse y magnetometro:",mag_y)
    print("Asse z magnetometro:",mag_z)

    time.sleep_ms(500)

    #Inizializzazione e visualizzazione dei dati del giroscopio
    gyro_x, gyro_y, gyro_z = lsm.read_gyro()

    print("Asse x Giroscopio:",gyro_x)
    print("Asse y Giroscopio:",gyro_y)
    print("Asse z Giroscopio:",gyro_z)

    time.sleep_ms(500)







