from typing import Optional, List
from bs4 import BeautifulSoup, Tag
import requests
from dataclasses import dataclass
from utils.data_type_converter import convert_number
import pymysql
import utils.DataTypeConverter as dtc

@dataclass
class KosdaqPrice:
    cur_price: float
    cur_volume: float
    cur_volume_price: float
    cur_volume_personal: float
    cur_volume_foreigner: float
    cur_volume_inst_fund: float
    cur_volume_prg_pos: float
    cur_volume_prg_neg: float


def get_realtime_price() -> KosdaqPrice:
    rt_kosdaq_url = 'https://finance.naver.com/sise/sise_index.naver?code=KOSDAQ'
    req = requests.get(rt_kosdaq_url, headers={'User-agent': 'Mozilla/5.0'})
    dom = BeautifulSoup(req.text, "html.parser")
    cur_price = dom.select_one('em#now_value').text
    cur_volume = dom.select_one('td#quant').text
    cur_volume_price = dom.select_one('td#amount').text
    cur_volume_personal = dom.select_one('dl.lst_kos_info').select_one(':nth-child(2)').select_one('span').text
    cur_volume_forg = dom.select_one('dl.lst_kos_info').select_one(':nth-child(3)').select_one('span').text
    cur_volume_inst_fund = dom.select_one('dl.lst_kos_info').select_one(':nth-child(4)').select_one('span').text

    cur_volume_prog_pos = dom.select_one('dl.lst_kos_info').select_one(':nth-child(6)').select_one('span').text
    cur_volume_prog_neg = dom.select_one('dl.lst_kos_info').select_one(':nth-child(7)').select_one('span').text

    # print(cur_volume_personal + '|' + cur_volume_forg + '|' + cur_volume_inst_fund + '|'
    #       + cur_volume_prog_pos + '|' + cur_volume_prog_neg)
    # print(cur_price + "|" + cur_volume + "|" + cur_volume_price + "|")

    return KosdaqPrice(cur_price=dtc.convert_number(cur_price),
                       cur_volume=dtc.convert_number(cur_volume),
                       cur_volume_price=dtc.convert_number(cur_volume_price),
                       cur_volume_personal=dtc.convert_uck(cur_volume_personal),
                       cur_volume_foreigner=dtc.convert_uck(cur_volume_forg),
                       cur_volume_inst_fund=dtc.convert_uck(cur_volume_inst_fund),
                       cur_volume_prg_pos=dtc.convert_uck(cur_volume_prog_pos),
                       cur_volume_prg_neg=dtc.convert_uck(cur_volume_prog_neg)
                       )
