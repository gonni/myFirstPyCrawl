from time import sleep
from typing import Optional, List
from bs4 import BeautifulSoup, Tag
import requests
from dataclasses import dataclass
import utils.DataTypeConverter as dtc
import pymysql


class InvestorVolume:
    def __init__(self, date, personal, foreigner, company, finance, insurance, toosin, bank, etc_fin, gov_fund,
                 etc_comp):
        self.date = date
        self.personal = personal
        self.foreigner = foreigner
        self.company = company
        self.finance = finance
        self.insurance = insurance
        self.toosin = toosin
        self.bank = bank
        self.etc_fin = etc_fin
        self.gov_fund = gov_fund
        self.etc_comp = etc_comp


def crawl_investors(url) -> List[InvestorVolume]:
    # url = 'https://finance.naver.com/sise/investorDealTrendDay.naver?bizdate=20240726&sosok=&page=1'
    req = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    dom = BeautifulSoup(req.text, "html.parser")
    sel = dom.select('table.type_1 > tr > td.date2')

    sel_c: List[InvestorVolume] = []

    for trd in sel:
        tr = trd.parent
        sel_c.append(InvestorVolume(
            tr.select_one('td:nth-child(1)').text,
            dtc.convert_number(tr.select_one('td:nth-child(2)').text),
            dtc.convert_number(tr.select_one('td:nth-child(3)').text),
            dtc.convert_number(tr.select_one('td:nth-child(4)').text),
            dtc.convert_number(tr.select_one('td:nth-child(5)').text),
            dtc.convert_number(tr.select_one('td:nth-child(6)').text),
            dtc.convert_number(tr.select_one('td:nth-child(7)').text),
            dtc.convert_number(tr.select_one('td:nth-child(8)').text),
            dtc.convert_number(tr.select_one('td:nth-child(9)').text),
            dtc.convert_number(tr.select_one('td:nth-child(10)').text),
            dtc.convert_number(tr.select_one('td:nth-child(11)').text)
        ))
    return sel_c


def crawl_investor_volume2db(from_date='20240823', market_code='02', page=1):
    target_url = 'https://finance.naver.com/sise/investorDealTrendDay.naver?bizdate=%s&sosok=%s&page=%s' % (
    from_date, market_code, page)
    print(target_url)
    data = crawl_investors(target_url)

    for row in data:
        print(row.__dict__)

    conn = pymysql.connect(host='horusa', user='root', password='root', db='zio', charset='utf8mb4')
    cur = conn.cursor()

    # sql = "INSERT INTO CRAWL_INVESTOR_DAILY_VOLUME(TYPE_CODE, DATEON, PERSONAL, FOREIGNER, COMPANY, FINANCE, INSURANCE, TOOSIN, BANK, ETC_FIN, GOV_FUND, ETC_FUND) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); "

    sql = f"""
    INSERT INTO CRAWL_INVESTOR_DAILY_VOLUME(TYPE_CODE, DATEON, PERSONAL, FOREIGNER, COMPANY, FINANCE, INSURANCE, TOOSIN, BANK, ETC_FIN, GOV_FUND, ETC_FUND)  
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
        TYPE_CODE=values(TYPE_CODE),
        DATEON=values(DATEON),
        PERSONAL=values(PERSONAL),
        FOREIGNER=values(FOREIGNER),
        COMPANY=values(COMPANY),
        FINANCE=values(FINANCE),
        INSURANCE=values(INSURANCE),
        TOOSIN=values(TOOSIN),
        BANK=values(BANK),
        ETC_FIN=values(ETC_FIN),
        GOV_FUND=values(GOV_FUND),
        ETC_FUND=values(ETC_FUND)
    """

    for row in data:
        try:
            cur.execute(sql, (
            market_code, row.date, row.personal, row.foreigner, row.company, row.finance, row.insurance, row.toosin,
            row.bank, row.etc_fin, row.gov_fund, row.etc_comp))
        except Exception as e:
            print('error ---> ' + row.date + ' --> ' + str(e))

    conn.commit()
    conn.close()

print('save crawled data ..')
crawl_investor_volume2db(page=2)