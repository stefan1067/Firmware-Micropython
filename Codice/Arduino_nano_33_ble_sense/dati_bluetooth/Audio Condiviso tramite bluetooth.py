#Trasferimento valore medio uscita audio del canale sinistro e del canale destro
import image, audio, time
from ulab import numpy as np
from ulab import scipy as sp
from ulab import utils
import time
import lsm9ds1
from board import LED
from machine import Pin, I2C
from ubluepy import Service, Characteristic, UUID, Peripheral, constants
#Imposto parametri da passare ad audio.init(canale e size)
CHANNELS = 1
SIZE = 256//(2*CHANNELS)

raw_buf = None  #Contenitore dei byte ascoltati dal microfono inizializzato a None
fb = image.Image(SIZE+50, SIZE, image.RGB565, copy_to_fb=True)

#Inizializza audio.init(ascolta direttamente microfono interno)
audio.init(channels=CHANNELS, frequency=16000, gain_db=80, highpass=0.9883)

#Funzione che riempe il buffer audio ogni volta che viene ascoltato qualcosa dal microfono
def audio_callback(buf):

    global raw_buf
    if (raw_buf == None):
        raw_buf = buf

# Start audio streaming
audio.start_streaming(audio_callback)

#Funzioni per disegnare grafico nel Frame Buffer
def draw_fft(img, fft_buf):
    fft_buf = (fft_buf / max(fft_buf)) * SIZE
    fft_buf = np.log10(fft_buf + 1) * 20
    #audio_char.write(fft_buf)
    color = (0xFF, 0x0F, 0x00)
    for i in range(0, SIZE):
        img.draw_line(i, SIZE, i, SIZE-int(fft_buf[i]), color, 1)

def draw_audio_bar(img, level, offset):
    blk_size = SIZE//10
    color = (0xFF, 0x00, 0xF0)
    blk_space = (blk_size//4)
    for i in range(0, int(round(level/10))):
        fb.draw_rectangle(SIZE+offset, SIZE - ((i+1)*blk_size) + blk_space, 20, blk_size - blk_space, color, 1, True)


#Inizializzazione Bluetooth
def event_handler(id, handle, data):
    global periph, service, notif_enabled

    if id == constants.EVT_GAP_CONNECTED:
        #  'connected'
        LED(1).on()
    elif id == constants.EVT_GAP_DISCONNECTED:
        #  'disconnected'
        LED(1).off()
        periph.advertise(device_name="Audio Sensor", services=[service])
    elif id == constants.EVT_GATTS_WRITE:
        if int(data[0]) == 1:
            notif_enabled = True
        else:
            notif_enabled = True

#Parto con Led spento, ovvero indica nessuna connessione bluetooth
LED(1).off()

notif_enabled = False
uuid_service=UUID("0X2BEF")     #Service Audio
uuid_audio  = UUID("0x2B83")  # Audio characteristic


#Inizializzazione Servizio e porte audio
service = Service(uuid_service)
audio_props = Characteristic.PROP_READ|Characteristic.PROP_NOTIFY
audio_attrs = Characteristic.ATTR_CCCD
audio_char = Characteristic(uuid_audio, props=audio_props, attrs=audio_attrs)

service.addCharacteristic(audio_char)


periph = Peripheral()
periph.addService(service)
periph.setConnectionHandler(event_handler)
periph.advertise(device_name="Audio", services=[service])


while (True):
    #Una volta che viene connesso l'arduino al bluetooth, viene abilitato il microfono e la condivisione dei dati
    if notif_enabled:
      if (raw_buf != None):
            pcm_buf = np.frombuffer(raw_buf, dtype=np.int16)
            #print(pcm_buf)
            raw_buf = None

            if CHANNELS == 1:
                fft_buf = utils.spectrogram(pcm_buf)
                l_lvl = int((np.mean(abs(pcm_buf[1::2])) / 32768)*100)
                prova_l=float(l_lvl)
                sx_audio=('Audiosx:{:>8.1f}'.format(prova_l))
                audio_char.write(sx_audio)
                print("La media dell'uscita audio del canale sx vale:",sx_audio)
                #l_lvl->Livello audio sinistro

                #prova=('Audio_sx:{:>8.3f}'.format(l_lvl)
                #audio_char.write(prova)

            else:
                fft_buf = utils.spectrogram(pcm_buf[0::2])
                l_lvl = int((np.mean(abs(pcm_buf[1::2])) / 32768)*100)
                #media livello audio del canale sinistro
                prova_l=float(l_lvl)
                sx_audio=('Audiosx:{:>8.1f}'.format(prova_l))
                audio_char.write(sx_audio)
                print("La media dell'uscita audio del canale sx vale:",sx_audio)
                #audio_char.write(prova_audio)
                #Media del livello audio del canale destro
                r_lvl = int((np.mean(abs(pcm_buf[0::2])) / 32768)*100)
                prova_r=float(r_lvl)
                dx_audio=('Audiosx:{:>8.1f}'.format(prova_r))
                audio_char.write(dx_audio)
                print("La media dell'uscita audio del canale dx vale:",dx_audio)

            fb.clear()
            draw_fft(fb, fft_buf)
            #audio_char.write( draw_fft(fb, fft_buf))
           # service.addCharacteristic(audio_char)
            draw_audio_bar(fb, l_lvl, 0)
            #service.add_frame(draw_audio_bar(fb, l_lvl, 0))
            if CHANNELS == 2:
                draw_audio_bar(fb, r_lvl, 25)
            fb.flush()



# Stop streaming
audio.stop_streaming()
