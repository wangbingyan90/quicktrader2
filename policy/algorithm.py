import pandas as pd
# 该方法没有加权平均
# import talib as ta
# dw['slowk'], dw['slowd']  = ta.STOCH(dw['high'].values, dw['low'].values, dw['close'].values, fastk_period=9, slowk_period=3, slowk_matype=1, slowd_period=3, slowd_matype=1)
def calc_kdj(df):
    low_list = df['low'].rolling(9, min_periods=9).min()
    low_list.fillna(value=df['low'].expanding().min(), inplace=True)
    high_list = df['high'].rolling(9 , min_periods=9 ).max()
    high_list.fillna(value=df['high'].expanding().max(), inplace=True)
    rsv = (df['close'] - low_list) / (high_list - low_list) * 100
    df['k'] = pd.DataFrame(rsv).ewm(com=2).mean()
    df['d'] = df['k'].ewm(com=2).mean()
    df['j'] = 3 * df['k'] - 2 * df['d']
    df['kintend'] = df['k'].diff()

    df['kdj'] = df['k']-df['d']
    df['kdjintend']  = df['kdj'].diff()
    df['kdjcrossintend'] = df['kdj'] > df['kdjintend']*-1
    # df['kdj'] = 0
    series = df['k']>df['d']
    # df.loc[series[series == True].index, 'kdj'] = 1
    df['kdjcross'] = 0
    df.loc[series[(series == True) & (series.shift() == False)].index, 'kdjcross'] = 1
    df.loc[series[(series == False) & (series.shift() == True)].index, 'kdjcross'] = -1
    return df

def calc_macd(df, fastperiod=12, slowperiod=26, signalperiod=9):
    ewma12 = df['close'].ewm(span=fastperiod,adjust=False).mean()
    ewma26 = df['close'].ewm(span=slowperiod,adjust=False).mean()
    df['dif'] = ewma12-ewma26
    df['dea'] = df['dif'].ewm(span=signalperiod,adjust=False).mean()

    df['difintend'] = df['dif'].diff()
    series2 = df['dif'] > df['difintend']*-1
    df['difcross'] = 0
    df.loc[series2[(series2 == True) & (series2.shift() == False)].index, 'difcross'] = 1
    df.loc[series2[(series2 == False) & (series2.shift() == True)].index, 'difcross'] = -1


    df['macd'] = (df['dif']-df['dea'])*2
    df['macdintend']  = df['macd'].diff()


    series = df['macd']>0
    df['macdcross'] = 0
    df.loc[series[(series == True) & (series.shift() == False)].index, 'macdcross'] = 1
    df.loc[series[(series == False) & (series.shift() == True)].index, 'macdcross'] = -1
    return df

def calc_ma(df):
    df['ma3'] = df['close'].rolling(window=5).mean()
    
    df['is3'] = df['ma3'] < df['close']
    return df
