# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from gpio_const import outpins, gndpins, pin_position_num, RESET_NUM

class Util7segLED():

    def __init__(self):
        self.sleep = 0.004
        self.gpio_init()

    def gpio_init(self):
        GPIO.setmode(GPIO.BOARD)
        # 各ピンの初期化
        for i in range(4):
            GPIO.setup(gndpins[i],GPIO.OUT)
            GPIO.output(gndpins[i],True)

        for i in range(7):
            GPIO.setup(outpins[i], GPIO.OUT)
            GPIO.output(outpins[i], False)


    # カレント桁数の番号を点灯
    def lighting(self, n):
        out = pin_position_num[n]

        for i in range(7):
            if out & (0b1000000 >> i):
                GPIO.output(outpins[i], True)
            else:
                GPIO.output(outpins[i], False)


    # 桁数を変える
    def lightDigit(self, n):
    	for i in range(4):
    		if i == n:
    			GPIO.output(gndpins[i], False)
    		else:
    			GPIO.output(gndpins[i], True)


    # 4桁の時分の数字を渡して7セグLEDをダイナミック点灯させる
    def dynamicLighting(self, hm):

        hm_l = [int(i) for i in hm]
        for i in range(4):

            n = display[i]

            self.lighting(RESET_NUM)     # 点灯をリセット
            self.lightDigit(i)           # 点灯する桁数
            self.lighting(pin_position_num[n]) # 点灯
            time.sleep(self.sleep)       # ウェイト


    def lightOut(self):
        GPIO.cleanup()


LED = Util7segLED()
for i in range(10):
    LED.dynamicLighting(1050)

LED.lightOut()