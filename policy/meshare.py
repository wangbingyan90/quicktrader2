import json
import requests
import pandas as pd
import time
import tushare as ts
from urllib.request import urlopen, Request
import os


# ------------------------------------------------获取ticks-----------------------------

bs_type = {'1':u'买入',
           '2': u'卖出',
           '4': u'-'}


# 获取当天的tick
def get_today_ticks(code=None, retry_count=3, pause=0.001):
    url = 'http://push2ex.eastmoney.com/getStockFenShi?pagesize=6644&amp;ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzfscj&pageindex=0&;id=%s&sort=1&ft=1&code=%s&market=%s&_=%s'
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            maker = 1
            if str(code)[:2] == '12':
                maker =  0
            re = Request(url%(code, code, maker, int(time.time())))
            lines = urlopen(re, timeout=10).read()
            lines = json.loads(lines)
            lines = lines['data']['data']
            df = pd.DataFrame(lines)  
            df = df.rename(columns={'t': 'time', 'p': 'price', 'v': 'vol', 'bs': 'type'})
            df = df[['time', 'price', 'vol', 'type']]
            df['price'] = df['price'].map(lambda x: x/1000)
            df['type'] = df['type'].map(lambda x: bs_type[str(x)])
            df['time'] = df['time'].map(lambda x: str(x).zfill(6))
        except Exception as e:
            print(e)
        else:
            # print(df[-11:])
            return df[12:]
    raise IOError('网络失败')

def get_today_min_data_bytick(code):
    liprice = []
    lilow = []
    lihigh = []
    liday = []
    dw = get_today_ticks(code)
    for i in range(int(len(dw)/20)):
        d = dw[i*20:i*20+19]
        # print(d)
        day = d['time'].values.tolist()[-1]
        price = d['price'].values.tolist()[-1]
        low = d['price'].min()
        high = d['price'].max()
        
        # print(day,high,low,price)
        liprice.append(price)
        lilow.append(low)
        lihigh.append(high)
        liday.append(day)

    return pd.DataFrame({'day':liday,'close': liprice, 'low':lilow,'high':lihigh})

# print(get_today_min_data_bytick('128052'))

# 获取任意一天
def get_tick_data(code,date='2020-08-18',src='tt'):
    return ts.get_tick_data(code,date,src='tt') # tick没有当天

# dw = ts.get_tick_data('128052',date = '2020-08-20',src='tt')
# for i in range(len(dw)):
#     print(dw[i:i+1])

def get_day_min_data_bytick(code,date = '2020-08-18'):
    str1 = '30'
    # print(date)
    if os.path.isfile('C://Users//wby//Documents//date//'+code+date+'.pkl'):
        dw=pd.read_pickle('C://Users//wby//Documents//date//'+code+date+'.pkl')
    else:
        dw = ts.get_tick_data(code,date,src='tt')
        dw.to_pickle('C://Users//wby//Documents//date//'+code+date+'.pkl')
    # print(dw)
    i1 = 1
    liprice = []
    lilow = []
    lihigh = []
    liday = []
    for i in range(0,int(len(dw))):
        if str1 == dw.time[i][3:5]:
            pass
        elif dw.time[i][:5] == '09:25' or dw.time[i][:5] == '09:29':
            i1 = i+1
        else:
            d = dw[i1:i]
            # print(d)
            i1 = i
            str1 = dw.time[i][3:5]

            day = d['time'].values.tolist()[-1]
            price = d['price'].values.tolist()[-1]
            low = d['price'].min()
            high = d['price'].max()
            
            # print(day,high,low,price)
            liprice.append(price)
            lilow.append(low)
            lihigh.append(high)
            liday.append(day)
    return pd.DataFrame({'day':liday,'close': liprice, 'low':lilow,'high':lihigh})


# print(get_day_min_data_bytick('128052','2020-08-21'))
# dw = ts.get_tick_data('128052',date = '2020-08-21',src='tt')
# print(dw)
# dw = get_today_ticks('128052')
# print(dw.time[19])

# 快 但 时间上有偏差
def get_quit_day_min_data_bytick(code,date = '2020-08-18'):
    liprice = []
    lilow = []
    lihigh = []
    liday = []
    dw = ts.get_tick_data(code,date,src='tt')
    for i in range(int(len(dw)/20)):
        d = dw[i*20:i*20+19]
        day = d['time'].values.tolist()[-1]
        price = d['price'].values.tolist()[-1]
        low = d['price'].min()
        high = d['price'].max()
        
        # print(day,high,low,price)
        liprice.append(price)
        lilow.append(low)
        lihigh.append(high)
        liday.append(day)

    return pd.DataFrame({'day':liday,'close': liprice, 'low':lilow,'high':lihigh})

# print(get_day_min_data_bytick('128052'))

# 获取当前的一条
def get_realtime_quotes(code):
    return ts.get_realtime_quotes(code)

# print(get_realtime_quotes('128052'))


# ------------------------------------------------时分图-----------------------------

def get_min_data(code="sh113581",len="238",long = '1'):
    '''
    len:数量长度 120 238
    long:时间区间 仅支持 1 5 15 30 60 120 240

    '''
    url = "https://quotes.sina.cn/cn/api/jsonp_v2.php/=/CN_MarketDataService.getKLineData"
    params = {
        "symbol": code,
        "scale": long,
        "datalen": len,
    }
    r = requests.get(url, params=params)
    str1 = r.text.split('=(')[1].split(");")[0]
    temp_df = pd.DataFrame(json.loads(str1))
    for key in ['open','high','low','close','ma_price5','ma_volume5','ma_price10','ma_volume10','ma_price30','ma_volume30']:
        temp_df[key] = pd.to_numeric(temp_df[key])
    # return temp_df.iloc[:,[0,4,6,8,10]]
    return temp_df

# for row in get_min_data('sz128052').iterrows():
#     print(row[1]['day'])


# ------------------------------------------------文本数据-----------------------------
def getOpen(str):
    f = open(str)
    liprice = []
    lilow = []
    lihigh = []
    liday = []
    for line in f:
        data = line.split()
        price = float(data[4])
        low = float(data[3])
        high = float(data[2])
        day = data[0]
        liprice.append(price)
        lilow.append(low)
        lihigh.append(high)
        liday.append(day)
    return pd.DataFrame({'day':liday,'close': liprice, 'low':lilow,'high':lihigh})

# dw = meshare.getOpen('C://Users//wby//Documents//2.txt')
