"""
AISHI

S | SolidCapacitor

AO | A0
A1 | A1
A2 | A2

0B | Voltage Code2W.Vsadasd
0E | Voltage Code2.5W.V
0G | Voltage Code4W.V
0J | Voltage Code6.3W.V
0Q | Voltage Code7W.V
1A | Voltage Code10W.V
1C | Voltage Code16W.V
1E | Voltage Code25W.V
1V | Voltage Code35W.V
1H | Voltage Code50W.V


Y |  Capacitance-25～+20
K |  Capacitance-10～+10
M |  Capacitance-20～+20
Q |  Capacitance-10～+30
V |  Capacitance-10～+20
A |  Capacitance-0～+20
C |  Capacitance-5～+20
J |  Capacitance+6～+20
B |  Capacitance-10～-20
W |  Capacitance-15～+15
G |  Capacitance-15~+20
L |  Capacitance-35~+10

4R7 | Capacitance4.7uF
100 | Capacitance10uF
150 | Capacitance15uF
220 | Capacitance22uF
330 | Capacitance33uF
470 | Capacitance47uF
680 | Capacitance68uF
820 | Capacitance82uF
101 | Capacitance100uF
151 | Capacitance150uF
181 | Capacitance180uF
201 | Capacitance200uF
221 | Capacitance220uF
331 | Capacitance330uF
471 | Capacitance470uF
561 | Capacitance560uF

A09 | 7.3×4.3L*Wmm 0.9mm
A19 | 7.3×4.3L*Wmm 1.9mm
A28 | 7.3×4.3L*Wmm 2.8mm



R04 | E.S.R4.0mΩ
R10 | E.S.R10mΩ
R06 | E.S.R6.0mΩ
R12 | E.S.R12mΩ
R07 | E.S.R7.0mΩ
R15 | E.S.R15mΩ
R09 | E.S.R9.0mΩ
R40 | E.S.R40mΩ
RA0 | E.S.R100mΩ
RB0 | E.S.R200mΩ
RA2 | E.S.R120mΩ
RB2 | E.S.R220mΩ


XXX | Special Code


"""

# 导入pymysql模块
import pymysql

# 连接database
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       db='1bomspider',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
# 得到一个可以执行SQL语句并且将结果作为字典返回的游标
# cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

# 定义要执行的SQL语句
sql = """
SELECT
	data
FROM
	riec_part_number_rule_code 
WHERE
	rule_id = ( SELECT id FROM riec_part_number_rule WHERE brand = 'AISHI(爱华集团)' );
"""

# 执行SQL语句
cursor.execute(sql)
ret = cursor.fetchall()
# print(ret)
d1 = []
# print(len(ret))
for data in ret:
    # 循环以\r\n分割取值
    data_res = data['data'].split('\r\n')
    # 以 | 分割
    data_list = [i.split('|') for i in data_res]
    d1.append(data_list)

d2 = {}
for i, data in enumerate(d1):
    data_dic = {i[0].strip(): i[1].strip() for i in data}
    d2[i+1] = data_dic
print(d2)

l1 = []
for i in d2:
    s1 = r''
    for j in d2[i]:
        s1 = s1 + j + '|'
    else:
        l1.append(s1)
print(l1)
rule_dict = {f"RE_RULE_{k}": rf"^{l1[k-1][:-1]}$" for k in range(1, len(l1) + 1)}
print(rule_dict)

# 关闭光标对象
cursor.close()

# 关闭数据库连接
conn.close()


