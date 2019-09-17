# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019/1/15 7:39 PM
#   FileName = Cabinet

import requests


class Cabinet(object):
    def __init__(self):
        self.api_url = 'http://prod.yaobili.com/device/monitoringList?type=normal&pageNo={}&pageSize=100'

    def _get_data(self):
        response = requests.get(self.api_url.format('1'))
        result = response.json()
        pages = int(result.get('page'))
        data = result.get('rows')
        if pages > 1:
            for page in range(2,pages+1):
                resp = requests.get(self.api_url.format(page))
                data += resp.json().get('rows')

        return data

    def check(self):
        """
        check 函数，为监控的主函数，返回状态和异常数据
        :return: 返回报警等级：status_num ，报警数据：alarm_data
        """
        data = self._get_data()
        alarm_data = {
            '1': [],
            '2': [],
            '3': []
        }
        status_num = 0
        for item in data:
            vmid = item.get('vmId')
            deviceMode = (int(item.get('deviceMode')) if item.get('deviceMode') else 0)
            # 系统维护
            if not item.get('slsStatus') and not deviceMode:
                d1 = {
                    '柜机ID': vmid,
                    '柜机名称': item.get('organName')
                }
                alarm_data.get('1').append(d1)
                status_num = (1 if status_num <1 else status_num)
            # 应用状态
            if not item.get('ssStatus') and not deviceMode:
                d3 = {
                    '柜机ID': vmid,
                    '柜机名称': item.get('organName')
                }
                alarm_data.get('3').append(d3)
                status_num = (3 if status_num <3 else status_num)

        return {'status_num':status_num,'alarm_data':alarm_data}

    def __getattr__(self, item):
        return None
