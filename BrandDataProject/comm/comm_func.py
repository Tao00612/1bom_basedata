"""
所有品牌通用方法
"""
import os
import sys
import time

sys.path.append(os.path.abspath('../..'))
import re
from ToolProject.mysql_utils.mysql_conf import MYSQL_CONFIG_DEV
from ToolProject.mysql_utils.mysql_conn import MysqlPooledDB


class CommFixedLengthBrand:
    """
    品牌通用类
    """

    def __init__(self, r_rule, bra_rule, *args, **kwargs):
        """
        :param r_rule: 正则表达式
        :param bra_rule: 正则表达式通过对应的参数
        :param args:
        :param kwargs:
        """
        self.r_rule = r_rule
        self.bra_rule = bra_rule
        super(CommFixedLengthBrand, self).__init__(*args, **kwargs)
        self.conn, self.cursor = MysqlPooledDB(MYSQL_CONFIG_DEV['1bom.1bomSpider']).connect()

    def create_read_data(self, sql_data):
        """
        sql_data 是数据库 模糊查找的数据
        :return:
        """
        useful_list = []
        for i in sql_data:
            # 循环判断 是否匹配正则 匹配成功进入下一步
            if res := re.match(self.r_rule, i['kuc_name']):
                # 数据产品参数字符串拼接
                # 循环正则匹配得到的数据
                s1 = "||".join(self.bra_rule[j][v] for j, v in enumerate(res.groups(), 1))
                useful_list.append(('kuc_id', i['kuc_name'], s1))

        return useful_list

    def query_data(self, sql_str):
        """
        执行sql 得到结果返回
        :param sql:
        :return:
        """
        self.cursor.execute(sql_str)
        res = self.cursor.fetchall()
        return res
