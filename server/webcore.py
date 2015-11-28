# -*- coding: utf-8 -*-
# テンプレートエンジン（jinja2）対応版

from jinja2 import Environment, FileSystemLoader
import cgi, os, sys, io

class Webcore:
    def __init__(self, debug=False, basepath='./'):
        self.debug = debug
        self.method = os.environ.get('REQUEST_METHOD', "")

        # テンプレートエンジンの準備
        self.env = Environment(loader=FileSystemLoader(basepath, encoding='utf8'))
        # テンプレートに割り当てる値をkey:valueで格納
        self.conv = {}

        # print()実行時にLANGの環境変数が参照されるため、utf-8で上書きする
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

        if debug:
            import cgitb
            cgitb.enable()   # エラーが出たときにブラウザに表示する

    def get(self, file, lconv={}):
        tmpl =  self.env.get_template(file)
        buff = tmpl.render(lconv)

        return buff

    def put(self, file, lconv={}):
        tmpl =  self.env.get_template(file)

        self.conv.update(lconv)
        output = tmpl.render(self.conv)

        print('Content-type: text/html; charset=utf-8') # header
        print()                                         # end of header
        print(output)                                   # output
        sys.exit()

    def is_post(self):
        return 'POST' == self.method

    def is_get(self):
        return 'GET' == self.method
