# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2018/12/16 上午1:46
#   FileName = config

"""
    config.py
    ~~~~~~~~~~~~~~~~~

    Interview questions setting file

"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


class Config:
    PROJECT_DIR = BASE_DIR

    # Mysql 配置
    MYSQL_HOST = 'rm-wz9xqe04o3v4y20sj.mysql.rds.aliyuncs.com'
    MYSQL_PORT = 3306
    MYSQL_USER = 'ybl2018'
    MYSQL_PASSWORD = 'ybl2018@'
    MYSQL_DB_NAME = 'monitoring'

    # 邮箱SMTP设置，
    MAIL_HOST = "smtp.exmail.qq.com"
    MAIL_PORT = 465  # 使用ssl端口
    MAIL_USER = 'wangyx@yaobili.com'  # 自行修改
    MAIL_PASSWD = 'Wyx379833553'  # 自行修改

    # 报警隔离时间，同一个报警，在过了隔离时间后才会重新报警,单位：h
    ISOLATE_TIME = 24

    # 配置监控邮件接收人
    MAIL_SENDEE = ['wangyx@yaobili.com','jiangcq@yaobili.com']

    # 配置监控项,
    # k：主题，为自定义的监控项名称
    # v：此监控的主类，在此类中定义监控，并返回监控结果数据
    MONITOR_DICT = {
        'cabinet': 'monitors.cabinet.Cabinet'
    }

    # 报警方式配置
    # k：主题，此主题是MONITOR_DICT中配置的监控项
    # v：配置报警模版类，可配置多种，则同时触发发送多种报警
    ALARM_DICT = {
        'cabinet': ['template.mail.MailAlarmTemplate']
    }

    # 告警历史记录配置
    # k: 主题，此主题是MONITOR_DICT中配置的监控项
    # v：配置记录类，可配置多种，则同时进行多种记录
    RECORD_DICT = {
        'cabinet': ['record.offline.OfflineRecord']
    }


    def __init__(self):
        pass

    def __getattr__(self, item):
        return None


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


# Default using Config settings, you can write if/else for different env
config = DevelopmentConfig()
