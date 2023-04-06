# Kevin McAleer
# April 2023
# This program reads the sound level from the microphone 
# and turns the built-in LED on if the sound level is less than 60000

from machine import Pin, ADC

noise = ADC(Pin(26))
led = Pin(25, Pin.OUT)

sound_level = 0

while True:
    # Read the sound level
    sound_level = noise.read_u16()

    # If the sound level is less than 60000, turn the built-in LED on
    if sound_level < 60000:
        led.value(1)
    else:
        led.value(0)