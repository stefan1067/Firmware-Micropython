import image, audio, time
from ulab import numpy as np
from ulab import scipy as sp
from ulab import utils

#Imposto parametri da passare ad audio.init(canale e size)
CHANNELS = 1
SIZE = 256//(2*CHANNELS)


raw_buf = None  #Contenitore dei byte ascoltati dal microfono inizializzato a None

fb = image.Image(SIZE+50, SIZE, image.RGB565, copy_to_fb=True)  #Immagine del frame buffer

#Inizializza audio.init(ascolta direttamente microfono interno)
audio.init(channels=CHANNELS, frequency=16000, gain_db=80, highpass=0.9883)

#Funzione che riempe il buffer audio ogni volta che
def audio_callback(buf):
    global raw_buf
    if (raw_buf == None):
        raw_buf = buf

# Start audio streaming
audio.start_streaming(audio_callback)

#Funzioni per disegnare grafico all'interno del Frame Buffer
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

#Microfono ascolta in continuazione
while (True):
    if (raw_buf != None):
        pcm_buf = np.frombuffer(raw_buf, dtype=np.int16)
        raw_buf = None

        if CHANNELS == 1:
            fft_buf = utils.spectrogram(pcm_buf)
            #Livello audui medio dei dati del canale sx
            l_lvl = int((np.mean(abs(pcm_buf[1::2])) / 32768)*100)
            print(l_lvl)
        else:
            fft_buf = utils.spectrogram(pcm_buf[0::2])
            #livello audio medio del canale sx e dx
            l_lvl = int((np.mean(abs(pcm_buf[1::2])) / 32768)*100)
            print(l_lvl)
            r_lvl = int((np.mean(abs(pcm_buf[0::2])) / 32768)*100)
            print(r_lvl)

        fb.clear()  #Riaggiorna frame buffer
        #Chiama funzioni per disegnare nel frame buffer
        draw_fft(fb, fft_buf)
        draw_audio_bar(fb, l_lvl, 0)

        if CHANNELS == 2:
            draw_audio_bar(fb, r_lvl, 25)
        fb.flush()

# Stop streaming
audio.stop_streaming()
