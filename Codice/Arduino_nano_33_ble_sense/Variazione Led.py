from board import LED
import time

led_red = LED(1)
led_green = LED(2)
led_blue = LED(3)

while (True):

    # Turn on LEDs
    led_red.on()
    led_green.off()
    led_blue.off()

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
