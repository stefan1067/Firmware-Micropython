from machine import Pin
from machine import SPI, Pin
import time
import machine
import struct
from struct import *
#I valori sono garantiti alla frequenza di clock di 10 MHz per SPI
#inizializzazione di SPI
spi = SPI(baudrate=10000000, polarity=1, phase=0, sck=Pin("PB10"), mosi=Pin("PC3"), miso=Pin("PC2"))
#spi = SPI(0, mode=SPI.MASTER, baudrate=10000000, polarity=0, phase=0, pins=("PB10","PC3","PC2"))#
#polarity assume il valore di 0 e 1 e serve per abilitare le modalità di lettura e scrittura all'interno della scheda
#baudrate serve per indicare la frequenza di clock da utilizzare.
# Setup
green = Pin("PC5", Pin.OUT)
red = Pin("PB0", Pin.OUT)
#attivazione del bluethoot->Impostare PC4 a livello elevato
bluethoot=Pin("PC4",Pin.OUT)
bluethoot.value(0)
time.sleep(10)
bluethoot.value(1)

#Abilitazione della modalità SPI per CS
SPI2_CS=Pin("PC13",Pin.OUT)
#SPI2_CS.value(0)	#Quando CS assume valore 0 viene abilitato

#Inizializzazione dell'accelerometro
CTRL1_XL=0x10
#Accelerometro inizializzato quando è in modalità Power Down
ACC=0000
#comando di scrittura per impostare il valore dell'accelerometro
#pi.write(b'0000',0x10)
#
#Si abilita il giroscopio tramite il comando
print("prova")
#Loop
while True:
	red.value(0)
	green.value(1)
	time.sleep(1)
	green.value(0)
	red.value(1)
	time.sleep(1)
	#byte_data=spi.read(2,0xB0)
	
	#Conversione da byte a float
	#	float_value=struct.unpack('f',byte_data)
	#print(float_value)
	
	#print(float_value)
	#conversione
	#conversione=float_value*0.061*9.8
	#print(conversione)
	#print(spi.read(8,0xB0))
	#Conversione dei dati dell'accelerometro
	#print(conversione=(dati*9.8))
	#print(conversione)
	#print(spi.read(8,0xB0))
	#spi.readinto(CTRL1_XL,)ù

	#il valore dei vari dati convertiti deve essere tra -127 e +127
	#lettura dati di un registro
	#Abilitazione della modalità SPI per CS
	
	#Inizializzazione dell'accelerometro in modalità Low
	buf = bytearray(1)
	buf[0] = 0b10000000  | 0x4B
	SPI2_CS.value(0)	#Quando CS assume valore 0 viene abilitato
	spi.write(buf)
	#print(spi.readinto(buf, 1))
	SPI2_CS.value(1)	#Quando CS assume valore 0 viene abilitato
	#configurazione dell'accelerometro
	SPI2_CS.value(0)	#Quando CS assume valore 0 viene abilitato
	bufAcc=bytearray(2)
	bufAcc[0]=0x10
	bufAcc[1]=0xB0	#imposto accelerometro sulla modalità a bassa frequenza
	spi.write(bufAcc)
	#print(spi.read(bufAcc,1))
	SPI2_CS.value(1)	#Quando CS assume valore 0 viene abilitato
	#lettura dei vari dati dell'accelerometro
	
	#Impostazione dei vari datio dell'acceleto
	bufx=bytearray(1)
	bufy=bytearray(1)
	bufz=bytearray(1)
	bufx[0] = 0b10000000  | 0x28	#selezione del registro in modalità low
	bufy[0]= 0b10000000  | 0x2A
	bufz[0]= 0b10000000  | 0x2C
	SPI2_CS.value(0)	#Quando CS assume valore 0 viene abilitato
	spi.write(bufx)
	spi.write(bufy)
	spi.write(bufz)
	spi.readinto(bufx, 1)
	spi.readinto(bufy,1)
	spi.readinto(bufz,1)
	
	byte_sequence=spi.read(2,0x28)
	print(byte_sequence)
	# Converti in decimale
	decimal_number = int.from_bytes(byte_sequence, 'big')

	# Stampa il risultato
	#0x28 indica modalità a bassa frequenza
	print("Accelerometro asse x convertito",decimal_number)	#nostro valore in decimale
	#Conversione del valore in binario per comprendere il valore di MSB e per capire se il valore convertito dovrebbe essere negativo o positivo
	binary_string = bin(decimal_number)
	print(binary_string)#Convertito valore decimale in binario(unione di 2 byte in formato esadecimale)
	#Per capire se valore è negativo controllo MSB
	#Se MSB vale 1 allora valore negativo, inverto tutti i bit e metto +1 per avere valore convertito
	#Controllo del valore binario
	taglia_num=binary_string[2:]	#taglia 0b->Valore che indica che il numero è binario
	print(taglia_num)	#stampo numero per controllare che non varia il valore
	
    #Controllo del valore MSB per comprendere se numero positivo o negativo
	if binary_string[0] == '1':	#Utilizzo : al posto delle parentesi
		inverted_string = ''.join('1' if bit == '0' else '0' for bit in binary_string)
		negative_decimal = -(int(inverted_string, 2))
		print("Valore decimale negativo:", negative_decimal)
	else:
		positive_decimal = int(binary_string, 2)
		print("Valore decimale:", positive_decimal)
	
    
	# Calcola il complemento a due
    #Controllo del valore MSB per comprendere se numero positivo o negativo
	# Converti la stringa binaria in un intero
        
	#print("asse x",spi.read(2,0x28))
	#print("asse Y",spi.read(2,0x2A))
	#print("asse Z",spi.read(2,0x2C))
	
	#Conversione dei vari dati
	#print(struct.unpack("ff", spi.read(2,0x028)))
    
	#print("asse x",spi.readinto(buf1, 2))

	#print("Asse x",spi.read(2,0x28))
	#float_value=struct.unpack('f',byte_data)[0]
	#print(conversione)
	#print("Asse x",spi.read(2,0x29))
	#print("Asse y",spi.read(8,0x74))
	#print("Asse z",spi.read(8,0x75))
	SPI2_CS.value(1)	#Quando CS assume valore 0 viene abilitato