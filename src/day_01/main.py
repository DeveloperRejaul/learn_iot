from machine import Pin  # type: ignore
import time

led = Pin(2, Pin.OUT)   # GPIO 2 = অন-বোর্ড LED

while True:
    led.value(1)        # LED জ্বলবে
    time.sleep(1)
    led.value(0)        # LED নিভবে
    time.sleep(1)
