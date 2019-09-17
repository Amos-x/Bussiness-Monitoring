# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-12 11:50
#   FileName = mysql

import pymysql
from config import config as CONFIG


class MysqlConnect():
    def __init__(self, host, port, user, password, db, charset='utf8'):
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self._connect()

    def _connect(self):
        self.conn = pymysql.Connect(
            host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.db, charset=self.charset
        )
        self.cursor = self.conn.cursor()

    # 执行sql文件
    def exec_sql_file(self, path):
        """ 成功执行返回True， 反之False """
        print('执行 {}'.format(path))
        with open(path, 'r+') as f:
            sql_list = f.read().split(';')[:-1]  # sql文件最后一行加上;
            sql_list = [' '.join(['' if '--' in y else y for y in x.split('\n')]) for x in sql_list]
        try:
            for sql_item in sql_list:
                self.cursor.execute(sql_item)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print('{} 文件执行错误 : {}'.format(path,e))
            return False

    # 执行sql语句
    def exec_sql(self, sql):
        """ 成功执行返回True， 反之False """
        if isinstance(sql,str):
            try:
                self.cursor.execute(sql)
                self.conn.commit()
                result = self.cursor.fetchall()
                result = (result if result else True)
                return result
            except:
                self.conn.rollback()
                return False
        else:
            raise TypeError("Sql only accept str type")

    def close(self):
        self.cursor.close()
        self.conn.close()


def get_conner():
    return MysqlConnect(CONFIG.MYSQL_HOST,CONFIG.MYSQL_PORT,CONFIG.MYSQL_USER,CONFIG.MYSQL_PASSWORD,CONFIG.MYSQL_DB_NAME)
