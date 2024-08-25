import crawl.CrawlKosdaqInvestors as cki
import crawl.CrawlKosdaqPrice as ckp
import pymysql.cursors
import pandas as pd


def sync_kosdaq_data():
    ckp.save_data()
    cki.crawl_investor_volume2db()
    print('crawl today completed ..')


conn = pymysql.connect(host='horusa',
                       user='root',
                       password='root',
                       db='zio',
                       charset='utf8mb4',
                       autocommit=True,
                       cursorclass=pymysql.cursors.DictCursor)


def exec_query(sql) -> pd.DataFrame:
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    # print(result.count())
    cur.close()
    df = pd.DataFrame(result)
    return df


def get_daily_kosdaq():
    sql = 'select * from CRAWL_MARKET_DAILY_DATA'
    return exec_query(sql)


def get_daily_investors_volume():
    sql = "select DATEON, PERSONAL, FOREIGNER, COMPANY, FINANCE, INSURANCE, TOOSIN, BANK, ETC_FIN, GOV_FUND, ETC_FUND from CRAWL_INVESTOR_DAILY_VOLUME where TYPE_CODE='02'"
    return exec_query(sql)


# get_daily_kosdaq()
def create_ex_columns(df, name: str):
    # print(name + ' newly added ..')
    df[name + '_SUM_D5'] = df[name].rolling(5).sum().shift(1)
    df[name + '_AVG_D5'] = df[name].rolling(5).mean().shift(1)
    df[name + '_STD_D5'] = df[name].rolling(5).std().shift(1)
    df[name + '_SUM_D10'] = df[name].rolling(10).sum().shift(1)
    df[name + '_AVG_D10'] = df[name].rolling(10).mean().shift(1)
    df[name + '_STD_D10'] = df[name].rolling(10).std().shift(1)
    df[name + '_SUM_D20'] = df[name].rolling(20).sum().shift(1)
    df[name + '_AVG_D20'] = df[name].rolling(20).mean().shift(1)
    df[name + '_STD_D20'] = df[name].rolling(20).std().shift(1)


def get_kosdaq_target_data():
    investors_volume = get_daily_investors_volume()
    investors_volume = investors_volume.set_index('DATEON')
    investors_volume.sort_index(ascending=False, inplace=True)

    daily_kosdaq = get_daily_kosdaq()
    daily_kosdaq['DATEON'] = daily_kosdaq['DATEON'].str[2:]
    daily_kosdaq.set_index('DATEON').drop(labels=['TYPE_CODE'], axis=1)

    import pandas as pd

    merged = pd.merge(left=investors_volume, right=daily_kosdaq, how='inner', on='DATEON')

    merged.set_index('DATEON')
    merged.sort_index(ascending=False, inplace=True)
    merged = merged.set_index('DATEON')
    merged = merged.drop(labels=['TYPE_CODE'], axis=1)

    feature_cols = ['PERSONAL', 'FOREIGNER', 'COMPANY', 'FINANCE', 'INSURANCE', 'TOOSIN', 'BANK', 'ETC_FIN', 'GOV_FUND',
                    'ETC_FUND',
                    'UP_DOWN_PER', 'VOLUME', 'VOLUME_AMT']

    for col in feature_cols:
        create_ex_columns(merged, col)

    merged['PRED_OUT_D3'] = merged['CLOSING_PRICE'].rolling(3).mean().shift(
        -2)  # merged['PRED_OUT'] = merged['CLOSING_PRICE'].shift(1)
    # merged[['DATEON', 'CLOSING_PRICE', 'PRED_OUT_D3', 'VOLUME_AMT', 'VOLUME_AMT_SUM_D5']]

    merged = merged.reset_index()
    merged = merged.set_index('DATEON')

    merged = merged.drop(['CLOSING_PRICE'], axis=1)
    # merged = merged.dropna()

    return merged


today_kosdaq = get_kosdaq_target_data().tail(1).drop('PRED_OUT_D3', axis=1)
train_data = get_kosdaq_target_data().dropna()

from pycaret.regression import *


def predict(train_data=train_data, today_data=today_kosdaq):
    s = setup(data=train_data, target='PRED_OUT_D3', session_id=123, normalize=True, normalize_method='zscore')
    best = compare_models(include=['et'])
    # evaluate_model(best)
    return predict_model(best, data=today_data)


res = predict()
# print('-- today -->' + today_kosdaq)
print(res)
