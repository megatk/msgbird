# -*- coding: utf-8 -*-

import cgi
import json
import datetime
from webcore import Webcore

class Form(Webcore):
    def __init__(self, debug=True):
        super().__init__(debug)

        f = cgi.FieldStorage()
        self.leave  = f.getfirst('leave', False)
        self.cancel = f.getfirst('cancel', False)

        # 3モードで分岐
        # get   ・・・ 初回アクセス
        # leave ・・・ 退社ボタン
        # cancel・・・ キャンセルボタン
        self.mode = 'get'
        if self.is_post():
            if self.leave: self.mode = 'leave'
            if self.cancel: self.mode = 'cancel'

    def import_cancel(self):
        return self.t.cancel

    def import_leave(self):
        return self.t.leave

if __name__ == '__main__':

    app = Form()
    if app.mode != 'get':
        f = open('kaneko.json', 'r', encoding='utf8')
        udata = json.loads(f.read())
        f.close()

        if app.mode == 'leave':
            hm = datetime.datetime.now().strftime('%H%M')
            # jsonファイルの書き込み
            udata['hm'] = hm
            udata['stop'] = "0"

        elif app.mode == 'cancel':
            udata['hm'] = ""
            udata['stop'] = "1"

        f = open('update.json', 'w', encoding='utf8')
        f.write(json.dumps(udata))

    # jsonファイルの読み込み
    f = open('update.json', 'r', encoding='utf8')
    udata = json.loads(f.read())

    hm   = udata['hm']
    stop = udata['stop']

    html, script = app.import_tmp(__file__) # ファイル名からhtmlとscriptを展開する
    leave = app.import_leave();
    cancel = app.import_cancel()

    if hm != "":
        # hh:mm形式にしたい
        leave = '退社 ' + hm

    if int(stop) == 1 or hm == "":
        # 退社ボタンを押していない or 既にキャンセル済みの場合は表示を出さない
        cancel = ""

    app.rander(html.format(script=script,leave=leave,cancel=cancel))