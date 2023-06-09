import image, audio, time
from ulab import numpy as np
from ulab import scipy as sp
from ulab import utils
from board import LED
import machine
import time
from machine import SPI,Pin,I2C

pin_a=machine.Pin(4,machine.Pin.IN, machine.Pin.PULL_UP)
#Pin scl
pin_scl=machine.Pin(16)
pin_dat=machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_UP)
#non importando librerie di altri controllori, prende direttamente Pin dell'arduino
#Pin digitale D10->28
#Pin TX->16
#creo buffer per salvare valori letti da spi
buf=bytearray(5)
#spi=machine.SPI(1)  #Utilizza il bus SPI 0
#Da pinout presente nella documentazione di arduino
#SPI CLOCK=D13->1
#SPI MOSI=D11->29
#SPI MISO=D12->30
#Collegaemto SPI

spi=SPI(1,baudrate=100000,polarity=0,phase=0,sck=Pin(1),mosi=Pin(29),miso=Pin(30))
spi.init(baudrate=1000000)#Imposto frequenza di lettura adeguata
#Devo collegare microfono e leggere dati corretti in quella posizione
spi.readinto(Pin(28),0x28)
#buf=spi.read(10,0xFF)
#print(spi.read(10))
print("Prova1")
CHANNELS = 1
SIZE = 256//(2*CHANNELS)
#received_data = spi.read(buf)
led_red = LED(1)
led_green = LED(2)
led_blue = LED(3)
#buffer = np.frombuffer(spi.read(spi, dtype=np.int16)
raw_buf = None
fb = image.Image(SIZE+50, SIZE, image.RGB565, copy_to_fb=True)
audio.init(channels=CHANNELS, frequency=16000, gain_db=80, highpass=0.9883)

#passo come parametro di lettura dei vari valori spi, il quale
def audio_callback(pin_dat):
    # NOTE: do Not call any function that allocates memory.
    global raw_buf
    if (raw_buf == None):
        raw_buf = pin_dat

# Start audio streaming
audio.start_streaming(audio_callback)

#SPI.recv(8,*,timeout=5000)
def draw_fft(img, fft_buf):
    fft_buf = (fft_buf / max(fft_buf)) * SIZE
    fft_buf = np.log10(fft_buf + 1) * 20
    color = (0xFF, 0x0F, 0x00)
    for i in range(0, SIZE):
        img.draw_line(i, SIZE, i, SIZE-int(fft_buf[i]), color, 1)

def draw_audio_bar(img, level, offset):
    blk_size = SIZE//10
    color = (0xFF, 0x00, 0xF0)
    blk_space = (blk_size//4)
    for i in range(0, int(round(level/10))):
        fb.draw_rectangle(SIZE+offset, SIZE - ((i+1)*blk_size) + blk_space, 20, blk_size - blk_space, color, 1, True)

while (True):
    print(pin_dat.value())
    print(pin_a.value())
   # print(raw_buf)
     # Turn on LEDs
    led_red.on()
    led_green.off()
    led_blue.off()
    print("Prova")
    # Wait 0.25 seconds
    time.sleep_ms(250)
    led_red.off()
    led_green.on()
    led_blue.off()
    time.sleep_ms(250)
    # Turn off LEDs
    led_red.off()
    led_green.off()
    led_blue.on()

    # Wait 0.25 seconds
    time.sleep_ms(250)
    if (raw_buf != None):
        pcm_buf = np.frombuffer(raw_buf, dtype=np.int16)
        raw_buf = None

        if CHANNELS == 1:
            fft_buf = utils.spectrogram(pcm_buf)
            l_lvl = int((np.mean(abs(pcm_buf[1::2])) / 32768)*100)
        else:
            fft_buf = utils.spectrogram(pcm_buf[0::2])
            l_lvl = int((np.mean(abs(pcm_buf[1::2])) / 32768)*100)
            r_lvl = int((np.mean(abs(pcm_buf[0::2])) / 32768)*100)

        fb.clear()
        draw_fft(fb, fft_buf)
        draw_audio_bar(fb, l_lvl, 0)
        if CHANNELS == 2:
            draw_audio_bar(fb, r_lvl, 25)
        fb.flush()

# Stop streaming
audio.stop_streaming()
