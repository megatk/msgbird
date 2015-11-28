# -*- coding: utf-8 -*-
# 7セグLEDの操作 実行時 第一引数に退社時間を渡す
import sys
from util7segLED import Util7segLED

def chkStop():
    f = open('stop.txt', 'r', encoding='ascii')
    stop = f.read(1)
    if int(stop) == 1:
        return True

    return False

LED = Util7segLED()
hm = sys.argv[1]

while True:
    if chkStop(): break # 停止フラグがあれば消灯する
    LED.dynamicLighting(hm)

LED.lightOut()