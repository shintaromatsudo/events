from machine import Pin
import time

red = Pin(11, Pin.OUT)
blue = Pin(15, Pin.OUT)
green = Pin(20, Pin.OUT)
yellow = Pin(16, Pin.OUT)

while True:
    red.value(1)
    green.value(0)
    time.sleep(0.1)
    blue.value(1)
    red.value(0)
    time.sleep(0.1)
    yellow.value(1)
    blue.value(0)
    time.sleep(0.1)
    green.value(1)
    yellow.value(0)
    time.sleep(0.1)