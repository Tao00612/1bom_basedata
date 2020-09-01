import os
import sys
sys.path.append(os.path.abspath('..'))
from BrandDataProject.comm.comm_func import CommFixedLengthBrand
from BrandDataProject.Setting import MIN_NUM_CHINOCERA as min_num
from BrandDataProject.Setting import SECTION_NUM_CHINOCERA as S_NUM
from BrandDataProject.Setting import RE_RULE_CHINOCERA as r_rule, brand_rule_chinocera as bra_rule

#   修改sql
#   在Settings文件根据dpf文件配置 最小数据长度,正则表达式,匹配规则参数具体,切片长度,切片数据


class PySql(CommFixedLengthBrand):

    def __init__(self, *args, **kwargs):
        super(PySql, self).__init__(min_num, S_NUM, r_rule, bra_rule, *args, **kwargs)

    @property
    def total_data_sql(self):
        """
        获取指定厂商号的sql
        :return:
        """
        return """
            select kuc_name from riec_stock_arrowcom 
            where kuc_name like 'HHV%' or kuc_name like 'HGC%' ;
        """

    def main_chinocera(self):
        ret = self.query_data(self.total_data_sql)
        list_data = self.create_read_data(ret)
        result_list = self.final_data_pattern(list_data)
        return result_list


if __name__ == '__main__':
    obj = PySql()
    obj.main_chinocera()
