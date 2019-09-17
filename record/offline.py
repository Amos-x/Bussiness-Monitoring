# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-12 15:46
#   FileName = cabinet

import uuid
import time
from pymysql.err import Error
from utils.mysql import get_conner


class OfflineRecord(object):
    def __init__(self):
        self.db = get_conner()
        self.now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def main(self, result, history):
        """ 主函数 """
        if not isinstance(result, list) and not None:
            raise ValueError('等级3，报警数据信息类型错误，应该为list')
        if not isinstance(history, list) and not None:
            raise ValueError('等级3，报警数据信息')
        for i in result:
            if i not in history:
                self. insert_offline_record(i)
            else:
                # 新数据和旧数据都有，证明正处于离线状态中，不做状态修改
                history.remove(i)
        for x in history:
            self.update_offline_record(x)

        # 关闭mysql连接
        self.db.close()

    def insert_offline_record(self, item):
        if self.db.exec_sql(
            """INSERT INTO `monitoring`.`cabinet_offline_record`(`id`, `cabinet_id`, `cabinet_name`, \
            `offline_starttime`) VALUES ('{}', '{}', '{}', '{}');""".format(uuid.uuid4(), item.get('柜机ID'),
                                                                           item.get('柜机名称'), self.now)
        ):
            print('插入新的离线记录: {}'.format(item))
        else:
            raise Error('插入数据错误: {}'.format(item))

    def update_offline_record(self, item):
        if self.db.exec_sql(
            """UPDATE `monitoring`.`cabinet_offline_record` SET `offline_endtime` = '{}' \
            WHERE `cabinet_id` = '{}' and `offline_endtime` is NULL;""".format(self.now, item.get('柜机ID'))
        ):
            print('更新结束时间成功: {}'.format(item))
        else:
            raise Error('更新数据错误: {}'.format(item))
