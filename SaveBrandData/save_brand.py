import os
import sys

sys.path.append(os.path.abspath('..'))
from ToolProject.mysql_utils.mysql_conf import MYSQL_CONFIG_DEV
from ToolProject.mysql_utils.mysql_conn import MysqlPooledDB
from BrandDataProject.brand import PySql
from BrandDataProject.brand import ExtractData


class SaveBrand:
    insert_base_data_list = []

    def __init__(self, sign, *args, **kwargs):
        """连接数据库"""
        self.sign = sign
        super(SaveBrand, self).__init__(*args, **kwargs)
        self.conn, self.cursor = MysqlPooledDB(MYSQL_CONFIG_DEV['1bom.1bomSpider']).connect()

    @property
    def query_data(self):
        """提取数据"""
        extract_data = ExtractData('RCXXXXXXXXXXXXXL', 'Yageo')
        bra_rule, r_rule = extract_data.create_parameter_dict()
        obj = PySql(r_rule, bra_rule, 'Yageo', '||', 'rule_2')
        result = obj.main()
        return result

    @property
    def insert_data_sql(self):
        """插入品牌标准型号数据表sql"""
        return """
            insert ignore into 
            riec_product(brand, name, brief, brand_id, category_id) 
            values(%s,%s,%s,%s,%s)
        """

    def get_brand_id(self):
        sql_brand_id = '''
            select id from `1bomProduct`.`riec_brand` where title = 'Yageo'
        '''
        self.cursor(sql_brand_id)
        brand_id = self.cursor.fetchone()[0]
        return brand_id

    def get_cate_id(self):
        sql_cate_id = '''
            SELECT categoryID FROM `1bomProduct`.`riec_category` WHERE `name` = '贴片电阻';
        '''
        self.cursor(sql_cate_id)
        cate_id = self.cursor.fetchone()[0]
        return cate_id

    def insert_data(self):
        """执行插入品牌标准型号数据表,返回一个列表"""
        # brand_id = self.get_brand_id()
        # cate_id = self.get_cate_id()
        brand_id = 1
        cate_id = 2
        data_list = [(i[0], i[1], i[2], brand_id, cate_id) for i in self.query_data]
        try:
            self.cursor.executemany(self.insert_data_sql, data_list)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        for i in data_list:
            data = i[2].split(self.sign)
            self.insert_base_data_list.append((self.sign.join(data), self.sign.join(data[:int(len(data) / 2)])))
        return self.insert_base_data_list

    @property
    def insert_base_data_sql(self):
        """插入基础产品数据表sql"""
        return """
            insert IGNORE into riec_product_base(parameter,parameter_show) values(%s,%s)
        """

    def insert_base_data(self, result):
        """执行插入基础产品数据表sql"""
        try:
            self.cursor.executemany(self.insert_base_data_sql, [(i[0], i[1],) for i in result])
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def update_product_id(self):
        sql = """
            UPDATE  riec_product t1
            LEFT JOIN
                    riec_product_base t2 
            ON      t1.brief = t2.parameter
            SET     t1.pid = t2.id
        """
        self.cursor.execute(sql)
        self.conn.commit()


if __name__ == '__main__':
    obj = SaveBrand('||')
    result = obj.insert_data()
    obj.insert_base_data(result)
    obj.update_product_id()
