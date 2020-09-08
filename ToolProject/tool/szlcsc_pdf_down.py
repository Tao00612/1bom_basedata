"""
用于下载立创指定品牌的pdf
"""
import asyncio
import random
import re
import httpx
from urllib.parse import urljoin
import os
import re
import sys

sys.path.append(os.path.abspath('..'))
from ToolProject.mysql_utils.mysql_conf import MYSQL_CONFIG_PROD
from ToolProject.mysql_utils.mysql_conn import MysqlPooledDB
from ToolProject.redis_utils.redis_conn import RedisConnPool
from ToolProject.redis_utils.redis_conf import REDIS_CONFIG_PROD

config_2 = REDIS_CONFIG_PROD.copy()
config_2['1bom.net']['db'] = 2
redis_2 = RedisConnPool(config_2['1bom.net']).connect()


async def query_pdf_code():
    conn, cursor = MysqlPooledDB(MYSQL_CONFIG_PROD['1bomProduct']).connect()

    sql = """
    SELECT
        kuc_pdf 
    FROM
        `1bomSpiderNew`.`riec_stock_others_attr` 
    WHERE
        kuc_shopid = 17 
        AND kuc_gid IN 
        ( SELECT kuc_gid FROM `1bomSpiderNew`.`riec_stock_others` 
        WHERE `kuc_parent` = '0-312-313-' AND `kuc_brname` = 'FH(风华)' AND `kuc_shopid` = '17' )
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    for i, data in enumerate(results, 1):
        file_path = f'C:/Users/admin/Desktop/work_pdf/风华/{i}.pdf'
        await down_pdf(data['kuc_pdf'], file_path)


async def down_pdf(pdf_code, file_name):
    """
    下载 pdf
    file_name
    """
    _pdf_base = 'https://atta.szlcsc.com/'
    _pdf_api = 'https://so.szlcsc.com/product/showProductPDFAndPCBJsonp?annexNumber={}'
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    }
    pdf_api_url = _pdf_api.format(pdf_code)
    proxy_list = redis_2.hkeys('zhima_proxy')
    http_proxy = random.choice(proxy_list)
    # http_proxy = http_proxy.replace('http', 'https')
    proxies = {
        # 'http': http_proxy,
        'https': http_proxy,
    }
    async with httpx.AsyncClient(proxies=proxies) as client:

        for _ in range(3):

            try:
                response = await client.get(pdf_api_url, timeout=30, headers=headers)
                if pdf_url := re.findall('annexUrl":\s*"(.*?)"', response.text, re.S):
                    pdf_url = urljoin(_pdf_base, pdf_url[0])
                    print(f'{pdf_url=}')
                    resp_pdf = await client.get(pdf_url, headers=headers)
                    await save_pdf(f'{file_name}', resp_pdf.content)
                    print(f'{pdf_code=} 下载')
                else:
                    print(f'{pdf_code=} 下载失败')
                return
            except:
                pass


async def save_pdf(file_name, file_content):
    """
    保存pdf到磁盘
    """
    with open(f'{file_name}', 'wb') as f:
        f.write(file_content)


if __name__ == '__main__':
    asyncio.run(query_pdf_code())
