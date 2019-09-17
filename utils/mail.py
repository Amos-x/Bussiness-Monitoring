# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2018/12/16 上午3:09
#   FileName = mail

"""
邮件工具，用于邮箱设置和邮件发送
根据业务不同，可以自定义不同类型的邮件类以供使用
自定义不同邮件类型时，继承基本 Mail 类，重写 init_message 方法即可实现自定义邮件内容类型
示例： ATTMail 为重写的附件邮件，其他类似
"""

import smtplib
import os
from config import config as CONFIG
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class Mail(object):
    """
    基础邮件类，发送文字内容邮件
    """
    def __init__(self):
        self.host = CONFIG.MAIL_HOST
        self.port = int(CONFIG.MAIL_PORT)
        self.user = CONFIG.MAIL_USER
        self.passwd = CONFIG.MAIL_PASSWD

    def _login(self):
        self.smtp = smtplib.SMTP_SSL(self.host,self.port)
        self.smtp.login(self.user,self.passwd)

    def init_message(self,mail_sendee,subject,content,*args,**kwargs):
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = Header(self.user, 'utf-8')
        message['To'] = Header(''.join(mail_sendee), 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        return message

    def sendmail(self,mail_sendee,subject,content,*args,**kwargs):
        self._login()
        message = self.init_message(mail_sendee,subject,content,*args,**kwargs)
        try:
            self.smtp.sendmail(self.user,mail_sendee,message.as_string())
            print('邮件发送成功')
        except Exception as e:
            print('邮件发送失败: %s' %e)
        self._quit()

    def _quit(self):
        self.smtp.quit()


class ATTMail(Mail):
    """
    自定义附件邮件类型，需要传参 attach_path ，支持字符串或列表
    如：'/home/test.txt' or ['/home/test1.txt','/home/test2.txt']
    """
    def init_message(self,mail_sendee,subject,content,*args,**kwargs):
        if not 'attach_path' in kwargs:
            raise ValueError('缺少附件参数 attach_path，无法发送附件邮件')
        message = MIMEMultipart()
        message['From'] = Header(self.user, 'utf-8')
        message['To'] = Header(''.join(mail_sendee), 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        # 添加附件
        attachs = (kwargs.get('attach_path') if isinstance(kwargs.get('attach_path'),list) else [kwargs.get('attach_path')])
        for attach in attachs:
            with open(attach,'rb') as f:
                att = MIMEText(f.read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att.add_header('Content-Disposition', 'attachment', filename=('gbk','',os.path.split(attach)[-1]))
            message.attach(att)
        # 返回message
        return message
