import pandas as pd

# df = pd.read_csv('../res/crawl_investor_daily_volume.csv').fillna(0)
df = pd.read_csv('../res/crwal_investor_stock_type.csv')
df = df.sort_values(by=['DATEON'], axis=0, ascending=True)
print(df)

df['FOR_BUY_D14'] = df.FOR_BUY.rolling(14).sum().shift(1)
df['FOR_BUY_D7'] = df.FOR_BUY.rolling(7).sum().shift(1)
df['COMP_BUY_D14'] = df.COMP_BUY.rolling(14).sum().shift(1)
df['COMP_BUY_D7'] = df.COMP_BUY.rolling(7).sum().shift(1)
df['DELTA_CORR'] = df.DELTA.rolling(3).sum().shift(1)
