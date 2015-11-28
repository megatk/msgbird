# -*- coding: utf-8 -*-
# 通知音の操作
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, False)

GPIO.setup(8, GPIO.OUT)
GPIO.output(8, False)

for i in range(5):
    GPIO.output(7, True)
    time.sleep(0.5)
    GPIO.output(7, False)
    time.sleep(0.5)

GPIO.cleanup(7)
GPIO.cleanup(8)