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
        self.msg    = f.getfirst('msg', "")

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

    def import_msg(self):
        return self.t.msg

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
            udata['msg'] = app.msg

        elif app.mode == 'cancel':
            udata['hm'] = ""
            udata['stop'] = "1"
            udata['msg'] = ""

        f = open('kaneko.json', 'w', encoding='utf8')
        f.write(json.dumps(udata))

    # jsonファイルの読み込み
    f = open('kaneko.json', 'r', encoding='utf8')
    udata = json.loads(f.read())

    hm      = udata['hm']
    stop    = udata['stop']

    html, script = app.import_tmp(__file__) # ファイル名からhtmlとscriptを展開する
    leave  = app.import_leave()
    cancel = app.import_cancel()
    msg    = app.import_msg()

    if hm != "":
        # hh:mm形式にしたい
        leave = '退社 ' + hm
    else:
        # 退社ボタンが既に押されている
        cancel = ""

    if len(udata['msg']) > 0:
        msg = udata['msg']

    app.rander(html.format(script=script,leave=leave,cancel=cancel,msg=msg))