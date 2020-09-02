import os
import re
import sys
import time

sys.path.append(os.path.abspath('..'))
from ToolProject.mysql_utils.mysql_conf import MYSQL_CONFIG_DEV
from ToolProject.mysql_utils.mysql_conn import MysqlPooledDB
from BrandDataProject.comm.comm_func import CommFixedLengthBrand
# from BrandDataProject.Setting import SECTION_NUM_AISHI as S_NUM
# from BrandDataProject.Setting import MIN_NUM_AISHI as min_num
# from BrandDataProject.Setting import RE_RULE_AISHI as r_rule, brand_rule_aishi as bra_rule

#   修改sql
#   在Settings文件根据dpf文件配置 最小数据长度,正则表达式,匹配规则参数具体,切片长度,切片数据


class ExtractData:

    def __init__(self, *args, **kwargs):
        self.parameter_dict = {}
        self.reg_list = []
        self.conn, self.cursor = MysqlPooledDB(MYSQL_CONFIG_DEV['1bom.1bomSpider']).connect()

    @property
    def extract_total_data(self):
        return """
        SELECT
            data
        FROM
            riec_part_number_rule_code
        WHERE
            rule_id = ( SELECT id FROM riec_part_number_rule WHERE brand = 'AISHI' );
        """

    def extract_sql(self):
        self.cursor.execute(self.extract_total_data)
        ret = self.cursor.fetchall()
        return ret

    def create_parameter_dict(self):
        for v, data in enumerate(self.extract_sql(), 1):
            # 循环以\r\n分割取值
            data['data'] = re.sub(' ', '', data['data'])
            data_res = data['data'].split('\r\n')
            # 以 | 分割
            data_list = [i.split('|') for i in data_res]
            # print(data_list)
            # 创建字典规则
            self.parameter_dict[v] = {i[0]: i[1] for i in data_list}
            # 创建正则表达式
            self.reg_list.append(f"({'|'.join(x[0] for x in data_list)})")

        reg_match_str = f"^{''.join(self.reg_list)}$"
        return self.parameter_dict, reg_match_str

    # def create_rule_dict(self):
    #     rule_list = []
    #     for i in self.parameter_dict:
    #         s1 = r''
    #         for j in self.parameter_dict[i]:
    #             s1 = s1 + j + '|'
    #         else:
    #             rule_list.append(s1)
    #     # 创建字典形式的规则
    #     rule_dict = {f"RE_RULE_{k}": rf"^{rule_list[k - 1][:-1]}$" for k in range(1, len(rule_list) + 1)}
    #     min_num = 15
    #     return rule_dict, min_num


class PySql(CommFixedLengthBrand):

    def __init__(self, *args, **kwargs):
        """
        min_num, S_NUM, r_rule, bra_rule  ExtractData类拿到
        :param args:
        :param kwargs:
        """
        extract_data = ExtractData()
        bra_rule, r_rule = extract_data.create_parameter_dict()
        super(PySql, self).__init__(r_rule, bra_rule, *args, **kwargs)

    @property
    def total_data_sql(self):
        """
        获取指定厂商号的sql
        :return:
        """
        return """
            select kuc_name from riec_stock_arrowcom 
            where kuc_name like 'SA0%' or kuc_name like 'SA1%' or kuc_name like 'SA2%';
        """

    def main(self):
        # 执行sql 得到厂商编号
        ret = self.query_data(self.total_data_sql)
        # 得到想要的数据
        list_data = self.create_read_data(ret)
        print(list_data)


if __name__ == '__main__':
    obj = PySql()
    obj.main()

