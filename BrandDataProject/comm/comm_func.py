"""
所有品牌通用方法
"""
import os
import sys
sys.path.append(os.path.abspath('../..'))
import re
from ToolProject.mysql_utils.mysql_conf import MYSQL_CONFIG_DEV
from ToolProject.mysql_utils.mysql_conn import MysqlPooledDB
# from BrandDataProject.Setting import MIN_NUM_CCTC as min_num
# from BrandDataProject.Setting import SECTION_NUM_CCTC as S_NUM
# from BrandDataProject.Setting import RE_RULE_CCTC as r_rule, brand_rule_cctc as bra_rule


class CommFixedLengthBrand:
    """
    品牌通用类
    """

    def __init__(self, min_num, S_NUM, r_rule, bra_rule, *args, **kwargs):
        """

        :param min_num: 最小的数据长度
        :param S_NUM: 切片相关的字典
        :param r_rule: 正则表达式
        :param bra_rule: 正则表达式通过对应的参数
        :param args:
        :param kwargs:
        """
        self.min_num = min_num
        self.S_NUM = S_NUM
        self.r_rule = r_rule
        self.bra_rule = bra_rule
        super(CommFixedLengthBrand, self).__init__(*args, **kwargs)
        self.conn, self.cursor = MysqlPooledDB(MYSQL_CONFIG_DEV['1bom.1bomSpider']).connect()

    def create_read_data(self, sql_data):
        """
        sql_data sql查询的数据
        读取文件,简单清洗不含规则的数据,
        :return:
        """
        useFul_list = []
        list_data = []
        for i in sql_data:
            # print(i)
            if len(i['kuc_name']) >= self.min_num:
                # 数据低于配置的数据全部清除
                useFul_list.append({'kuc_name': i['kuc_name']})

        for data in useFul_list:
            kuc_name = data['kuc_name']
            for x, y in self.S_NUM.items():
                # 根据配置文件 将数据切片 添加到列表
                kuc_name_t = [kuc_name[y[i]: y[i + 1]] for i in range(x)]
                list_data.append(kuc_name_t)
        return list_data

    def final_data_pattern(self, list_data):
        """
        list_data 通过的数据集
        根据 切片数据元组 和配置文件的正则表达式进行匹配, 将通过的数据保存在 result_list
        :return:
        """
        result_list = []
        for data in list_data:
            res_list = []
            for j in range(1, len(self.r_rule) + 1):
                if result := re.findall(self.r_rule[f'RE_RULE_{j}'], data[j - 1]):
                    # 正则匹配
                    res_list.append(self.bra_rule[j][result[0]])
                else:
                    res_list.clear()
                    break
            else:
                kuc_name = ''.join(data)
                param = '||'.join(res_list)
                res_tuple = ('kuc_id', kuc_name, param)
                result_list.append(res_tuple)

        return result_list

    def query_data(self, sql_str):
        """
        执行sql 得到结果返回
        :param sql:
        :return:
        """
        self.cursor.execute(sql_str)
        res = self.cursor.fetchall()
        return res
