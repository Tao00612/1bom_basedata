import os
import sys
sys.path.append(os.path.abspath('..'))
from ToolProject.mysql_utils.mysql_conf import MYSQL_CONFIG_DEV
from ToolProject.mysql_utils.mysql_conn import MysqlPooledDB
from BrandDataProject.chinocera_brand import PySql


class SaveBrand:
    insert_base_data_list = []

    def __init__(self, *args, **kwargs):
        """连接数据库"""
        super(SaveBrand, self).__init__(*args, **kwargs)
        self.conn, self.cursor = MysqlPooledDB(MYSQL_CONFIG_DEV['1bom.1bomSpider']).connect()

    @property
    def query_data(self):
        """提取数据"""
        obj = PySql()
        result = obj.main_chinocera()
        return result

    @property
    def insert_data_sql(self):
        """插入品牌标准型号数据表sql"""
        return """
            insert into riec_product(brand,name,brief) values(%s,%s,%s)
        """

    def insert_data(self):
        """执行插入品牌标准型号数据表,返回一个列表"""
        data_list = [('华瓷', i[1], i[2]) for i in self.query_data]
        self.cursor.executemany(self.insert_data_sql, data_list)
        self.conn.commit()
        for i in data_list:
            data = i[2].split('||')
            self.insert_base_data_list.append(("||".join(data), '||'.join(data[:int(len(data)/2)])))
        return self.insert_base_data_list

    @property
    def insert_base_data_sql(self):
        """插入基础产品数据表sql"""
        return """
            insert into riec_product_base(parameter,parameter_show) values(%s,%s)
        """

    def insert_base_data(self):
        """执行插入基础产品数据表sql"""
        self.cursor.executemany(self.insert_base_data_sql, [(i[0], i[1]) for i in self.insert_data()])
        self.conn.commit()

    def update_product_id(self):
        sql =  """
            
        """


obj = SaveBrand()
obj.insert_base_data()
