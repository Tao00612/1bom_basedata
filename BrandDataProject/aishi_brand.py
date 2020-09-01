import os
import sys
sys.path.append(os.path.abspath('..'))
from ToolProject.mysql_utils.mysql_conf import MYSQL_CONFIG_DEV
from ToolProject.mysql_utils.mysql_conn import MysqlPooledDB
from BrandDataProject.comm.comm_func import CommFixedLengthBrand
from BrandDataProject.Setting import SECTION_NUM_AISHI as S_NUM
# from BrandDataProject.Setting import RE_RULE_AISHI as r_rule, brand_rule_aishi as bra_rule

#   修改sql
#   在Settings文件根据dpf文件配置 最小数据长度,正则表达式,匹配规则参数具体,切片长度,切片数据


class ExtractData:

    def __init__(self, *args, **kwargs):
        self.parameter_dict = {}
        self.conn, self.cursor = MysqlPooledDB(MYSQL_CONFIG_DEV['1bom.1bomSpider']).connect()

    @property
    def extract_total_data(self):
        sql = """
        SELECT
            data
        FROM
            riec_part_number_rule_code
        WHERE
            rule_id = ( SELECT id FROM riec_part_number_rule WHERE brand = 'AISHI(爱华集团)' );
        """
        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        return ret

    def create_parameter_dict(self):
        for v, data in enumerate(self.extract_total_data, 1):
            # 循环以\r\n分割取值
            data_res = data['data'].split('\r\n')
            # 以 | 分割
            data_list = [i.split('|') for i in data_res]
            # print(data_list)
            self.parameter_dict[v] = {i[0].strip(): i[1].strip() for i in data_list}
        return self.parameter_dict

    def create_rule_dict(self):
        rule_list = []
        for i in self.parameter_dict:
            s1 = r''
            for j in self.parameter_dict[i]:
                s1 = s1 + j + '|'
            else:
                rule_list.append(s1)
        # 创建字典形式的规则
        rule_dict = {f"RE_RULE_{k}": rf"^{rule_list[k - 1][:-1]}$" for k in range(1, len(rule_list) + 1)}
        min_num = 15
        return rule_dict, min_num

    def create_section_num(self):
        pass


class PySql(CommFixedLengthBrand):

    def __init__(self, *args, **kwargs):
        """
        min_num, S_NUM, r_rule, bra_rule  ExtractData类拿到
        :param args:
        :param kwargs:
        """
        extract_data = ExtractData()
        bra_rule = extract_data.create_parameter_dict()
        r_rule, min_num = extract_data.create_rule_dict()
        super(PySql, self).__init__(min_num, S_NUM, r_rule, bra_rule, *args, **kwargs)

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
        # 将得到的编号简单进行数据清洗,并将数据切片得到列表中嵌套列表格式
        list_data = self.create_read_data(ret)
        # 用列表中嵌套的列表和配置文件的正则表达式进行匹配,匹配全部通过的值
        # 根据切片的数据和配置文件得到相对应的数据参数 放在result_list中
        result_list = self.final_data_pattern(list_data)
        print(result_list)
        return result_list


if __name__ == '__main__':
    obj = PySql()
    obj.main()
