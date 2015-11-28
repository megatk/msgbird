# -*- coding: utf-8 -*-
# jsonファイルの初期化
import json

file = 'kaneko.json';

f = open(file, 'r', encoding='utf8')
udata = json.loads(f.read())
udata['hm'] = ""
udata['stop'] = "1"
f.close()

f = open(file, 'w', encoding='utf8')
f.write(json.dumps(udata))
f.close()