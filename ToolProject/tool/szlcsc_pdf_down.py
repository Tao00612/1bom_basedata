"""
用于下载立创指定品牌的pdf
"""
import asyncio
import re
import httpx
from urllib.parse import urljoin


async def query_pdf_code():
    """
    查询pdf code
    """

    # await down_pdf(pdf_code)

async def down_pdf(pdf_code, file_name):
    """
    下载 pdf
    """
    _pdf_base = 'https://atta.szlcsc.com/'
    _pdf_api = 'https://so.szlcsc.com/product/showProductPDFAndPCBJsonp?annexNumber={}'
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    }
    pdf_api_url = _pdf_api.format(pdf_code)

    async with httpx.AsyncClient() as client:
        response = await client.get(pdf_api_url, timeout=30, headers=headers)
        if pdf_url := re.findall('annexUrl":\s*"(.*?)"', response.text, re.S):
            pdf_url = urljoin(_pdf_base, pdf_url[0])
            resp_pdf = await client.get(pdf_url, headers=headers)
            await save_pdf(f'{file_name}', resp_pdf.content)
        else:
            print(f'{pdf_code=} 下载失败')


async def save_pdf(file_name, file_content):
    """
    保存pdf到磁盘
    """
    with open(f'{file_name}', 'wb') as f:
        f.write(file_content)


if __name__ == '__main__':
    asyncio.run(down_pdf('17D9DF74756B1DE2296C67311B688FC3', '1.pdf'))