# -*- coding: utf-8 -*-

script = """
    <link rel="stylesheet" type="text/css" href="//ajax.googleapis.com/ajax/libs/jquerymobile/1.4.5/jquery.mobile.min.css" />
    <script type="text/javascript" src="js/jquery.min.js"></script>
    <script type="text/javascript" src="js/jquery.mobile-1.4.5.min.js"></script>
    <script type="text/javascript">
        $(function(){
            $.mobile.ajaxEnabled = false;
        });
    </script>
"""

html = '''
<!DOCTYPE html>
<html>
    <head>
    <title>おきがる伝言鳥</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">

    {script}
</head>
<body>
<div data-role="page">
    <div data-role="header" data-theme="b">
    <h1>おきがる伝言鳥(^▽^)</h1>
    </div>
    <div data-role="content">
        <form method="POST" action="form.py">
            <div class="ui-field-contain">
                <label for="msg">一言メッセージ</label>
                {msg}
            </div>
            <fieldset class="ui-grid">
            <div class="ui-block">{leave}</div>
            </fieldset>
        </form>
        {cancel}
    </div>
    <div data-role="footer" data-theme="b">
    <h4>Tomoki kaneko 2015</h4>
    </div>
</div>
</body>
</html>
'''

cancel = """
        <form method="POST" action="form.py">
            <fieldset class="ui-grid">
            <div class="ui-block"><input type="submit" value="取り消し" name="cancel" /></div>
            </fieldset>
        </form>
"""

leave = '<input type="submit" value="退社" name="leave" />'
msg = '<input id="msg" name="msg" type="text" value="" />'