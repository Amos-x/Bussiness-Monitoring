# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-14 17:49
#   FileName = run_server

from web.web_api import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
