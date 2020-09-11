import os
import re
import sys
import time

sys.path.append(os.path.abspath('..'))
from ToolProject.mysql_utils.mysql_conf import MYSQL_CONFIG_PROD
from ToolProject.mysql_utils.mysql_conn import MysqlPooledDB
from BrandDataProject.comm.comm_func import CommFixedLengthBrand


#  根据不同的品牌 写不同的sql


class ExtractData:

    def __init__(self, brand_exm, brand, *args, **kwargs):
        super(ExtractData, self).__init__(*args, **kwargs)
        self.parameter_dict = {}
        self.reg_list = []
        self.brand = brand
        self.brand_exm = brand_exm
        self.conn, self.cursor = MysqlPooledDB(MYSQL_CONFIG_PROD['1bomProduct']).connect()

    @property
    def extract_total_data(self):
        sql = '''
        SELECT
            data
        FROM
            riec_part_number_rule_code
        WHERE
            rule_id = ( SELECT id FROM riec_part_number_rule WHERE name = %s and brand = %s);
        '''
        return sql

    def extract_sql(self):
        self.cursor.execute(self.extract_total_data, (self.brand_exm, self.brand,))
        ret = self.cursor.fetchall()
        return ret

    def create_parameter_dict(self):
        for v, data in enumerate(self.extract_sql(), 1):
            # 循环以\r\n分割取值
            data['data'] = re.sub(' ', '', data['data'])
            data_res = data['data'].split('\r\n')
            # 以 | 分割
            data_list = [i.split('|') for i in data_res]
            # 创建字典规则
            self.parameter_dict[v] = {i[0]: i[1] for i in data_list}
            # 创建正则表达式规则
            self.reg_list.append(f"({'|'.join(x[0] for x in data_list)})")

        reg_match_str = f"^{''.join(self.reg_list)}$"
        return self.parameter_dict, reg_match_str


class PySql(CommFixedLengthBrand):

    def __init__(self, r_rule, bra_rule, brand, sign, rule, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        super(PySql, self).__init__(r_rule, bra_rule, brand, sign, rule, *args, **kwargs)

    @property
    def total_data_sql(self):
        """
        获取指定厂商号的sql
        :return:
        """
        return """
            select kuc_name from 1bomSpiderNew.`riec_stock_szlcsc`
            where kuc_name like 'RC%' --     OR kuc_name like 'R%' OR kuc_name like '2%';
        """

    def main(self):
        # 执行sql 得到厂商编号
        ret = self.query_data(self.total_data_sql)
        list_data = self.create_read_data(ret)
        print(list_data)
        print(len(list_data))
        return list_data


if __name__ == '__main__':
    # 第一个参数 是 数据库的例子
    # 第二个参数 是 例子品牌
    extract_data = ExtractData('RC0603XR-XXXXXXL', 'Yageo')
    bra_rule, r_rule = extract_data.create_parameter_dict()
    # bra_rule 品牌对应参数   r_rule 正则表达式
    # 第三参数 指定品牌     第四个参数 指定 分割符
    # 第五个参数 指定不同的品牌对应不同的规则方法
    obj = PySql(r_rule, bra_rule, 'Yageo', '||', 'rule_2')
    obj.main()


