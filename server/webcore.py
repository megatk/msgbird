# -*- coding: utf-8 -*-
import cgi, os, sys

class Webcore:
    def __init__(self, debug=True):
        self.debug = debug
        self.method = os.environ.get('REQUEST_METHOD', "")

        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

        if debug:
            import cgitb
            cgitb.enable()   # エラーが出たときにブラウザに表示する

    def rander(self,html):
        print('Content-type: text/html; charset=utf-8') # header
        print()                                         # end of header
        print(html)    # cgi.escapeでhtmlエスケープ

    def exithalfway(self,html):
        self.rander(html)
        sys.exit()

    def is_post(self):
        return 'POST' == self.method

    def is_get(self):
        return 'GET' == self.method

    def import_tmp(self, file): # テンプレートとスクリプトの動的呼び出し
        req = 'tm_' + file
        self.t = __import__(req[0:req.find('.')])
        return self.t.html, self.t.script