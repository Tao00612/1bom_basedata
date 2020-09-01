import os
import sys
sys.path.append(os.path.abspath('..'))
from BrandDataProject.comm.comm_func import CommFixedLengthBrand
from BrandDataProject.Setting import MIN_NUM_AISHI as min_num
from BrandDataProject.Setting import SECTION_NUM_AISHI as S_NUM
from BrandDataProject.Setting import RE_RULE_AISHI as r_rule, brand_rule_aishi as bra_rule

#   修改sql
#   在Settings文件根据dpf文件配置 最小数据长度,正则表达式,匹配规则参数具体,切片长度,切片数据


class PySql(CommFixedLengthBrand):
    def __init__(self, *args, **kwargs):
        """
        min_num, S_NUM, r_rule, bra_rule  配置文件的值传递到 CommFixedLengthBrand类中
        :param args:
        :param kwargs:
        """
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

    def main_aishi(self):
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
    obj.main_aishi()
