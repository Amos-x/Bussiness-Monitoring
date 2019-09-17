# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-14 10:25
#   FileName = web_api

import datetime
from utils.mysql import get_conner
from utils.common import get_time_difference
from flask import Flask
from flask import render_template
app = Flask(__name__)
db = get_conner()


@app.route('/')
def hello_world():
    sql = """select cabinet_id,cabinet_name,offline_starttime,unix_timestamp(now()) - unix_timestamp(offline_starttime) \
    as offline_duration from cabinet_offline_record where offline_endtime is NULL"""
    result = db.exec_sql(sql)
    if result and result is not True:
        data = []
        for i in result:
            i = list(i)
            i[3] = get_time_difference(i[3])
            data.append(tuple(i))
        return render_template('index.html', result=data)
    else:
        return '{} \nTrue: 数据为空，稍后再试 \nFalse: 内部错误，请检查'.format(result)


@app.route('/offline_times/<int:period>/')
def offline_times(period):
    start_time = datetime.datetime.today() - datetime.timedelta(days=period)
    sql = """select cabinet_id,cabinet_name,count(*) as offline_times from cabinet_offline_record \
    where offline_starttime > '{}' and offline_endtime is not NULL GROUP BY cabinet_id,cabinet_name \
    order by offline_times DESC;""".format(start_time)
    result = db.exec_sql(sql)
    if result and result is not True:
        return render_template('cishu.html', result=result)
    else:
        return '{} \nTrue: 数据为空，稍后再试 \nFalse: 内部错误，请检查'.format(result)


@app.route('/offline_duration/<int:period>/')
def offline_duration(period):
    start_time = datetime.datetime.today() - datetime.timedelta(days=period)
    sql = """select cabinet_id,cabinet_name,sum(UNIX_TIMESTAMP(offline_endtime)-UNIX_TIMESTAMP(offline_starttime)) as offline_duration \
    from cabinet_offline_record where offline_starttime > '{}' and offline_endtime is not NULL \
    GROUP BY cabinet_id,cabinet_name ORDER BY offline_duration DESC;""".format(start_time)
    result = db.exec_sql(sql)
    if result and result is not True:
        data = []
        for i in result:
            i = list(i)
            i[2] = get_time_difference(i[2])
            data.append(tuple(i))
        return render_template('duration.html',result=data)
    else:
        return '{} \nTrue: 数据为空，稍后再试 \nFalse: 内部错误，请检查'.format(result)
