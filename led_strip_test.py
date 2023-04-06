from machine import Pin, ADC
from time import sleep
import plasma
from plasma import plasma_stick
from time import ticks_ms

NUM_LEDS = 16

# set up the WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_GRB)

# start updating the LED strip
led_strip.start()

noise = ADC(Pin(26))
led = Pin("LED", Pin.OUT)

class Glow():
    r = 0
    g = 0
    b = 0
    max = 200
    up = True
    delay = 10
    
    def __init__(self):
        r = 0
        g = 0
        b = 0
        self.start_time = ticks_ms()
    
    def glow(self):
        
        if not ticks_ms() >= self.start_time + self.delay:
            return self.b
          
        self.start_time = ticks_ms()
        if self.up:
            if self.b <= self.max:
                self.b += 1
            else:
                self.up = False
        if not self.up:
            if self.b > 0:
               self.b -=1
            else:
                self.up = True
        
#         print(f'b func is {self.b}')
        return self.b
            

def rgb2hsv(r,g,b):
    r = r/255.0
    g = g/255.0
    b = b/255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    diff = cmax-cmin
    if cmax == cmin:
        h = 0
    elif cmax == r:
        h = (60 * ((g-b)/diff) + 360) % 360
    elif cmax == g:
        h = (60 * ((b-r)/diff) + 120) % 360
    elif cmax == b:
        h = (60 * ((r-g)/diff) + 240) % 360
    if cmax == 0:
        s = 0
    else:
        s = (diff/cmax) * 100
    v = cmax * 100
    return h, s, v

def hsv2rgb(h,s,v):
    s = s/100.0
    v = v/100.0
    c = v * s
    x = c * (1 - abs((h/60) % 2 - 1))
    m = v - c
    if h < 60:
        r,g,b = c,x,0
    elif h < 120:
        r,g,b = x,c,0
    elif h < 180:
        r,g,b = 0,c,x
    elif h < 240:
        r,g,b = 0,x,c
    elif h < 300:
        r,g,b = x,0,c
    else:
        r,g,b = c,0,x
    r = int((r+m)*255)
    g = int((g+m)*255)
    b = int((b+m)*255)
    return r,g,b

def light_on(r,g,b):
    for i in range(0,NUM_LEDS):
        led_strip.set_rgb(i, r, g, b)
        
def fade(r,g,b):
    h,s,v = rgb2hsv(r,g,b)

    if v > 0:
        v -= 1

    r,g,b = hsv2rgb(h,s,v)

    return r,g,b 

sound_level = 0
r = 0
g = 0
b = 0
glow = Glow()

while True:
    sound_level = noise.read_u16()
#     print (f'sound level: {sound_level}')
    if sound_level > 35000:
        led.value(1)
        r = 255
        b = 0
    else:
        if r == 0:
            b = glow.glow()
#             sleep(0.25)
            
        else:
            led.value(0)
            r,g,b = fade(r,g,b)
    light_on(r,g,b)

#     print(f'r:{r} g:{g} b:{b}')
    sleep(0.01)
    
#     sleep(0.01)
#     print(f'r,g,b {r},{g},{b}')
    