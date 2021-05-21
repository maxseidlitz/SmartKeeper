import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
FLOW_RATE = 125/60
MAX_TIME = 0
GLAS = 250


class wash():

    def wash_machine():

        pumplist = ['17', '27', '22']
        for p in pumplist:
            GPIO.setup(ing[0], GPIO.OUT)
            #print(f'infunction----------------')

        for p in pumplist:
            max_ml = 100
            waitTime = max_ml / FLOW_RATE
            GPIO.output(p, GPIO.LOW)
            time.sleep(waitTime)
            GPIO.output(p, GPIO.HIGH)
