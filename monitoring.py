# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2018/12/16 上午1:47
#   FileName = monitoring

from config import config as CONFIG
from concurrent.futures import ThreadPoolExecutor
from utils.common import FileModify
import importlib
import argparse
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class AutoMonitorManager(object):
    """
    自动监控报警类，多线程执行定义的监控项并报警
    """
    def __init__(self):
        self.monitor_dict = CONFIG.MONITOR_DICT
        self.alarm_dict = CONFIG.ALARM_DICT
        self.record_dit = CONFIG.RECORD_DICT

    def exec_monitor(self):
        """
        执行监控项check程序，检查监控状态
        """
        pool = ThreadPoolExecutor(10)
        for k,v in self.monitor_dict.items():
            pool.submit(self.task, k, v)

    def task(self,k,v):
        module_path, class_name = v.rsplit('.', 1)
        m = importlib.import_module(module_path)
        cls = getattr(m, class_name)
        result = cls().check()
        history_data = self.get_history_data(k)
        if history_data and isinstance(history_data,tuple):
            h_data = eval(history_data[2]).get('alarm_data').get('3')
        else:
            h_data = []
        self.record(k, result.get('alarm_data').get('3'), h_data)
        if result.get('status_num') > 1:
            print('{} 监控项告警'.format(k))
            self.trigger_alarm(k,result)
        else:
            print('无异常')

    def get_history_data(self,k=None):
        """  返回历史数据 """
        history_path = os.path.join(BASE_DIR, '.history')
        f = FileModify(history_path, autocreate=True)
        data = []
        for line in f.content().split('\n')[:-1]:
            data.append(tuple(line.split('||')))
        if k:
            for i in data:
                if i[0] == k:
                    return i
            return ()
        else:
            return data

    def record(self, k, result, history_data):
        """ 记录历史 """
        record_class = self.record_dit.get(k)
        print('{} 记录预警历史'.format(k))
        for record in record_class:
            module_path, class_name = record.rsplit('.',1)
            m = importlib.import_module(module_path)
            cls = getattr(m,class_name)
            cls().main(result,history_data)

    def is_alarm(self,k,result):
        """
        判断是否进行告警提示，相同告警进行拦截，相同告警在过了间隔时间后才会再次预警
        :return: 返回True，则可以进行告警，反之则否
        """
        history_path = os.path.join(BASE_DIR, '.history')
        f = FileModify(history_path, autocreate=True)
        data = self.get_history_data(k)
        now = int(time.time())
        if data and isinstance(data,tuple):
            alarm_data_3 = eval(data[2]).get('alarm_data').get('3')
            if alarm_data_3 == result.get('alarm_data').get('3'):
                time_diff = now - int(data[1])
                if time_diff > 3600 * CONFIG.ISOLATE_TIME:
                    f.replace(data[1],now)
                    return True
                else:
                    return False
            else:
                f.replace('^{}.*'.format(k),'{}||{}||{}'.format(k,now,result))
                return True

        f.add('{}||{}||{}'.format(k,now,result))
        return True

    def trigger_alarm(self,k,result):
        """
        触发告警，根据返回的接口和配置的告警模版，进行告警
        """
        trigger_templates = self.alarm_dict.get(k)
        if self.is_alarm(k,result):
            print('{} 监控项发送预警信息'.format(k))
            for template in trigger_templates:
                module_path, class_name = template.rsplit('.',1)
                m = importlib.import_module(module_path)
                cls = getattr(m,class_name)
                cls().trigger(k,result)
        else:
            print('间隔时间内，忽略报警')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
    example:
        python3 monitoring check
    """)

    parser.add_argument('action',choices=['check'],type=str,help="选择执行操作")

    args = parser.parse_args()

    if args.action == 'check':
        AutoMonitorManager().exec_monitor()
