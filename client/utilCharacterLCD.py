# -*- coding: utf-8 -*-

# ★依存関係
# i2cをraspberryPiで使えるようにする必要がある
# smbusモジュールはRaspbianに入っていないため追加インストール
# $ sudo apt-get install python3-smbus

import smbus
import time
from lcd_const import CHANNEL, ADDRESS, C_ADR, W_ADR

# SB1602BW操作用クラス
class UtilCharacterLCD():

    def __init__(self):
        self.bus = smbus.SMBus(CHANNEL)

        self.init_SB1602B()

    def init_SB1602B(self):

        data = []

        # Function set
        # 上位4bit は 0011 固定
        data.append(0x38)   # 0b00111000
        data.append(0x39)   # 0b00111001

        # Internal OSC frequency
        # 上位4bitは 0001 固定
        data.append(0x14)   # 0b00010100

        # Contrast set
        #上位4bitは 0111 固定
        data.append(0x78)  # 0b01111000

        # Power/ICON/Contrast control
        # 上位4bitは 0101 固定
        data.append(0x5e)  # 0b01011110

        # Follower control
        data.append(0x6c)  # ob01101100

        self.bus.write_i2c_block_data(ADDRESS, C_ADR, data)
        # must wait 200ms
        time.sleep(0.25)

        data = []
        # Display ON/OFF control
        data.append(0x0c)
        # Clear Display
        data.append(0x01)
        # Entry mode set
        data.append(0x06)

        self.bus.write_i2c_block_data(ADDRESS, C_ADR, data)

        time.sleep(0.05)

    def writeLCD(self, string, pos=''):
        # 表示場所の指定
        if pos != '':
            # 先頭ビットは1にするため +128 する
            self.bus.write_byte_data(ADDRESS, C_ADR, int(pos) + 128)

        # 文字コード番号に1文字ずつ変換
        string = self.convertKanaFromHiragana(string)
        self.bus.write_i2c_block_data(ADDRESS, W_ADR, [int(s) for s in list(string)])

    def convertKanaFromHiragana(self, string):
        # ひらがなから半角カナへ変換
        conv = str.maketrans(
            'ぁぃぅぇぉゃゅょっあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん',
            'ｧｨｩｪｫｬｭｮｯｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝ'
        )
        return string.translate(conv).encode('sjis')

    def clearLCD(self):
        # ディスプレイの表示を消す
        self.bus.write_byte_data(ADDRESS, C_ADR, 0x01)

