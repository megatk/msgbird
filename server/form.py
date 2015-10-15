# -*- coding: utf-8 -*-
import cgi
import json
import datetime
from webcore import Webcore

class Form(Webcore):
    def __init__(self, debug=True):
        super().__init__(debug)

        self.filename = 'kaneko.json'

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


if __name__ == '__main__':

    app = Form()
    f = open(app.filename, 'r', encoding='utf8')
    udata = json.loads(f.read())
    f.close()

    if app.mode == 'leave':
        udata['hm'] = datetime.datetime.now().strftime('%H%M')
        udata['stop'] = "0"
        f = open(app.filename, 'w', encoding='utf8')
        f.write(json.dumps(udata))

    elif app.mode == 'cancel':
        udata['hm'] = ""
        udata['stop'] = "1"
        f = open(app.filename, 'w', encoding='utf8')
        f.write(json.dumps(udata))

    hm = ""
    if('' != udata['hm']):
        hm = datetime.datetime.strptime(udata['hm'], '%H%M').strftime('%H:%M')

    app.put('form.html',{'hm': hm })