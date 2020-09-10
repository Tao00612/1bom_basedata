"""
所有品牌通用方法
"""
import os
import sys

sys.path.append(os.path.abspath('../..'))
import re
from ToolProject.mysql_utils.mysql_conf import MYSQL_CONFIG_PROD
from ToolProject.mysql_utils.mysql_conn import MysqlPooledDB


class CommFixedLengthBrand:
    """
    品牌通用类
    """

    def __init__(self, r_rule, bra_rule, brand, sign, rule, *args, **kwargs):
        """

        :param r_rule:  生成的正则表达式
        :param bra_rule:  匹配成功之后 映射的参数关系
        :param brand:   产品的品牌
        :param sign:  指定分割符
        :param rule:  指定规则  rule_1 ....
        :param args:
        :param kwargs:
        """
        self.r_rule = r_rule
        self.bra_rule = bra_rule
        self.brand = brand
        self.sign = sign
        self.rule = rule
        super(CommFixedLengthBrand, self).__init__(*args, **kwargs)
        self.conn, self.cursor = MysqlPooledDB(MYSQL_CONFIG_PROD['1bomProduct']).connect()

    def create_read_data(self, sql_data):
        """
        sql_data 是数据库sql模糊查找的数据
        :return:
        """
        useful_list = []
        for data in sql_data:
            # 循环判断 是否匹配正则 匹配成功进入下一步
            if res := re.search(self.r_rule, data['kuc_name']):
                # 数据产品参数字符串拼接
                # 循环正则匹配得到的数据
                s1 = []
                for j, v in enumerate(res.groups(), 1):
                    if vv := self.bra_rule[j].get(v):
                        s1.append(vv)
                    else:
                        # 根据传来的规则参数 执行对应的规则方法
                        v = getattr(self, self.rule)(v, j)
                        # v = self.rule_1(v, j)
                        s1.append(v)
                s1_s = self.sign.join(s1)
                useful_list.append((self.brand, data['kuc_name'], s1_s))
        return useful_list

    def rule_1(self, v, j):
        '''
        处理能匹配正则 不能匹配参数字典的情况
        :param v:
        :param j: 下标
        :return:
        '''
        arg = list(self.bra_rule[j].values())[0]
        # 取单位符号 arg
        if len(v) == 3:
            # 处理数据3长度的情况
            if v.isdigit():
                # 处理数据全是数字的情况
                v = 'JUMPER' if v.count('0') == 3 else self.handle_data(v, arg)
            elif 'R' in v.upper():
                # 处理 R 情况数据
                v = v.replace('R', '.')
                v = str(float(v)) + arg
        elif len(v) == 4:
            # 处理数据4长度的情况
            if v.isdigit():
                # 处理数据全是数字的情况
                v = 'JUMPER' if v.count('0') == 4 else self.handle_data(v, arg)
            elif 'R' in v.upper():
                # 处理 R 情况数据
                v = v.replace('R', '.')
                v = str(float(v)) + arg
            else:
                # 处理最后一位为字母和数字的转换
                num, stem = (v[:-1], v[-1:])
                d_num = {
                    'J': 0.1,
                    'K': 0.01,
                    'L': 0.001,
                    'M': 0.0001,
                    'N': 0.00001,
                }
                v = str(round(int(num) * d_num.get(stem), 2))
                v = v[:v.index('.')] + arg if v.endswith('0') else v + arg

        return v

    def rule_2(self, data_str, index):
        arg = list(self.bra_rule[index].values())[0]
        d_stem = {
            'R': 'Ω',
            'K': 'KΩ',
            'M': 'MΩ'
        }
        parameter = ''
        for data_s in data_str:
            if data_s in d_stem:
                arg = d_stem[data_s]
                data_s = '.'
            parameter += data_s
        if parameter[-1] == '.':
            parameter = parameter[:-1]
        parameter += arg
        return parameter

    def query_data(self, sql_str):
        """
        执行sql 得到结果返回
        :param sql:
        :return:
        """
        self.cursor.execute(sql_str)
        res = self.cursor.fetchall()
        return res

    def handle_data(self, data, arg):
        """
        :param data: 需要转换的数据
        :param arg: 数据的单位
        :return:
        """

        def change_unit(num_unit_data: tuple, units: list, scale: int):
            """
            转换单位
            :type num_unit_data:
            :param units:
            :param scale:
            :return:
            """
            last_unit = units.index(num_unit_data[1])

            def change(n: float, unit):
                # 单位变小
                if n < 1 and last_unit != 0:
                    unit = max(0, unit - 1)
                    n *= scale
                # 单位变大
                elif n >= scale and last_unit != len(units) - 1:
                    unit = min(len(units), unit + 1)
                    n /= scale
                return '%g%s' % (n, units[unit])

            return change(float(num_unit_data[0]), last_unit)

        d_stem = {
            'l1': ['PF', 'NF', 'UF', 'MF', 'F'],
            'l2': ['R', 'K', 'M', 'G'],
            'l3': ['MW', 'W', 'KW'],
            'l4': ['mΩ', 'Ω', 'kΩ', 'MΩ'],
            'l5': ['μV', 'mV', 'V', 'KV', 'MV']
        }
        data = int(data[:-1]) * 10 ** int(data[-1])
        num_unit_data = (data, arg,)
        for _, y in d_stem.items():
            if arg in y:
                units = y
                break
        else:
            return
        scale = 1000
        return change_unit(num_unit_data, units, scale)
