# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019/1/16 2:35 PM
#   FileName = mail_template

"""
邮件发送模版，默认邮件告警内容模版
"""

from utils.mail import Mail
from config import config as CONFIG

MAIL_SENDEE = CONFIG.MAIL_SENDEE


class MailAlarmTemplate(object):
    """
    基础邮件告警类，根据返回状态不同，发送不同的模版信息
    1：低优先级报警，普通报警，不紧急，不太重要
    2：中优先级报警，重要的报警，不需要马上处理，但必须处理的重要报警
    3：高优先级告警，紧急情况，需马上处理
    """

    def _init_content(self,k,result):
        alarm_data = result.get('alarm_data')
        alarm_data = {
            '1': [str(i) for i in alarm_data.get('1')],
            '2': [str(i) for i in alarm_data.get('2')],
            '3': [str(i) for i in alarm_data.get('3')]
        }
        content = """
{} 业务告警
严重等级：{}
柜机掉线，请检查
完整数据：
严重等级：1 ，轻度问题，不紧急
{} 

严重等级：2 ，中度问题，略紧急
{}

严重等级：3 ，严重问题，需要尽快解决
{}
        """.format(k,result.get('status_num'),'\n'.join(alarm_data.get('1')),'\n'.join(alarm_data.get('2')),'\n'.join(alarm_data.get('3')))
        return content

    def trigger(self,k,result):
        """
        每个报警模版必有的主触发函数，通过此函数来触发进行报警。
        """
        mail = Mail()
        content = self._init_content(k,result)
        mail.sendmail(MAIL_SENDEE,k,content)
