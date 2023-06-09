import time
import hts221
from machine import Pin, I2C

#Connessione tramite I2C per la condivisione dei dati del sensore hts221
bus = I2C(1, scl=Pin(15), sda=Pin(14))
hts = hts221.HTS221(bus)

while (True):
    #Richiamo le funzioni incluse all'interno della libreria hts221 di openMV
    rH   = hts.humidity()
    temp = hts.temperature()

    #Valore in percentuale dell'umidità
    print ("rH: %.2f%%" %(rH))
    time.sleep_ms(100)

    #Valore della temperatura
    print(" T: %.2fC"%(temp))
