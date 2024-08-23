from typing import Optional, List
from bs4 import BeautifulSoup, Tag
import requests
from dataclasses import dataclass
from utils.data_type_converter import convert_number
import pymysql


@dataclass
class RealtimePriceCrawl:
    date: str
    closing_price: float
    up_down_per: float
    volume: float
    volume_amt: float


def get_kosdaq_daily_price(page=1):
    url = 'https://finance.naver.com/sise/sise_index_day.naver?code=KOSDAQ&page=%s' % page
    req = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    dom = BeautifulSoup(req.text, "html.parser")

    v_date = dom.select('tr > td.date')

    res: List[RealtimePriceCrawl] = []
    for v in v_date:
        res.append(RealtimePriceCrawl(
            date=v.parent.select_one(':nth-child(1)').text,
            closing_price=convert_number(v.parent.select_one(':nth-child(2)').text),
            up_down_per=convert_number(v.parent.select_one(':nth-child(4)').text.strip()),
            volume=convert_number(v.parent.select_one(':nth-child(5)').text),
            volume_amt=convert_number(v.parent.select_one(':nth-child(6)').text)
        )
        )
    return res


def save_data(crawled: List[RealtimePriceCrawl] = [], type_code='KOSDAQ'):
    conn = pymysql.connect(host='localhost', user='root', password='root', db='zio', charset='utf8mb4')
    cur = conn.cursor()

    sql = f"""
        INSERT INTO CRAWL_MARKET_DAILY_DATA(TYPE_CODE, DATEON, CLOSING_PRICE, UP_DOWN_PER, VOLUME, VOLUME_AMT)
        VALUES(%s, %s, %s, %s, %s, %s) as new
        ON DUPLICATE KEY UPDATE 
            TYPE_CODE=new.TYPE_CODE,
            DATEON=new.DATEON,
            CLOSING_PRICE=new.CLOSING_PRICE,
            UP_DOWN_PER=new.UP_DOWN_PER,
            VOLUME=new.VOLUME,
            VOLUME_AMT=new.VOLUME_AMT
    """

    for row in crawled:
        try:
            cur.execute(sql, (type_code, row.date, row.closing_price, row.up_down_per, row.volume, row.volume_amt))
        except Exception as e:
            print('duplicated key error --> ' + str(e))

    conn.commit()
    conn.close()

save_data(get_kosdaq_daily_price())