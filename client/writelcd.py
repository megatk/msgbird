# -*- coding: utf-8 -*-
import sys
from utilCharacterLCD import UtilCharacterLCD

LCD = UtilCharacterLCD()
msg = sys.argv[1]

# 初めに初期化しておく
LCD.clearLCD()

if len(msg) > 0:
    LCD.writeLCD(msg)

