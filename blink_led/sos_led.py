from gpiozero import LED
from time import sleep


DOT_PAUSE=0.5
LINE_PAUSE=0.2
WORD_PAUSE=1.5
LETTER_PAUSE=1

led = LED(17)

def dot(pause=DOT_PAUSE):
    led.on()
    sleep(pause)
    led.off()
    sleep(pause)
    return None

def line(pause=LINE_PAUSE):
    led.on()
    sleep(pause)
    led.off()
    sleep(pause)
    return None

def s():
    dot()
    dot()
    dot()
    return None

def o():
    line()
    line()
    line()
    return None

def sos():
    sleep(WORD_PAUSE)
    s()
    sleep(LETTER_PAUSE)
    o()
    sleep(LETTER_PAUSE)
    s()
    sleep(LETTER_PAUSE)
    return None

while True: 
    sos()
    