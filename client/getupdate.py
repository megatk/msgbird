# -*- coding: utf-8 -*-
# サーバー側のJsonファイル（退社時間の更新）を監視する
# （このファイルをcronで1分おきに実行するように設定する）
from urllib import request
import datetime
import json
import os

from const import baseurl, filepath, username, password # 設定のインポート

# BASIC認証用の handler を作成する
# http://docs.python.jp/3.3/howto/urllib2.html
password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, baseurl, username, password)
handler = request.HTTPBasicAuthHandler(password_mgr)

# handler を opener に実装する
opener = request.build_opener(handler)
# 作成した opener でリクエストする
request.install_opener(opener)

# HTTPヘッダーの指定
req = request.Request(filepath)

# If-Modified-Since ヘッダーでサーバー側に更新がない場合はJsonファイルを取得しない
# -9時間：サーバーのタイムゾーンに合わせる JST → GMT
# -1分：1分おきに更新を監視 → 1分前からみて更新があるかみてあげれば良い
now  = datetime.datetime.now()
diff = datetime.timedelta(hours=-9, minutes=-1)
adjust = now + diff
udate = adjust.strftime("%a, %d %b %Y %H:%M:%S GMT")
req.add_header("If-Modified-Since", udate)

try:
    response = request.urlopen(req)
    udata = json.loads(response.read().decode('utf8'))  # byte型から文字列に変換
    hm   = udata['hm']
    stop = udata['stop']

    if int(stop) == 1: # 取り消しの場合はLED点灯を止める
        os.system('echo 1 > stop.txt')
    elif hm != "": # 退社時間がある場合はLED点灯と通知音を鳴らす
        # 複数のファイルを実行するのでバックグラウンド実行とし getupdate.py側の処理は止めない
        os.system('echo 0 > stop.txt')
        os.system('sudo python3 notice.py &')
        os.system('sudo python3 lighthm.py ' + hm + ' &')

except request.HTTPError as e:
    # サーバー上のファイルが更新されていない場合 304となり終了
    # エラー処理は別途検討が必要
    print(e.reason)
