import meshare, algorithm
from colorama import init,Fore
import pandas as pd
init(autoreset=True)


def prints(str):
    print(str)
    pass

def printred(str):
    prints(Fore.RED+str)
    pass

def printgreen(str):
    prints(Fore.GREEN+str)
    pass

def printblue(str):
    prints(Fore.BLUE+str)
    pass

def printme(date,str1):
    # str1 = str(date['day'])+'#'*5+str(date['close'])[:6]+'#'*5+'macd:'+str(date['bar'])[:6]+'#'*5+'K:'+str(date['k'])[:6]+'#'*5+str(date['kdj'])[:6]
    if date['kdj'] > 0:
        if date['bar'] > 0:
            if date['macd'] > 0:
                printred(str1)
            else:
                printblue(str1)
        else:                                                
            printgreen(str1)
    else:
        prints(str1)


def get_share(code,date = '2020-08-21'):
    # dw = meshare.get_today_min_data_bytick(code)
    dw = meshare.get_day_min_data_bytick(code,date)
    dw = algorithm.calc_kdj(dw)
    dw = algorithm.calc_macd(dw)
    dw = algorithm.calc_ma(dw)
    return dw


def run(dw):
    have = False
    sum = 0
    p = 0
    for row in dw.iterrows():
        str1 = str(row[1]['day'])+'#'*5+str(row[1]['close'])[:5]+'#'*5+'ma3:'+str(row[1]['ma3'])[:6]+'#'*5+'macd:'+str(row[1]['bar'])[:4]+'#'*5+'K:'+str(row[1]['k'])[:4]+'#'*5+str(row[1]['kdj'])[:4]
        printme(row[1],str1)
        if not have:
            # 买入策略
            if row[1]['kdjcross'] == 1:
                printred('买入')
                p = row[1]['close']
                sum = sum - row[1]['close']
                have = True
            
        else:
            # 卖出策略
            if row[1]['kdjcross'] == -1:
                
                if row[1]['close']<p:
                    printred('赔钱:'+str(row[1]['close']-p))
                else:
                    prints('卖出:'+str(row[1]['close']-p))
                sum = sum + row[1]['close']
                have = False


            if row[1]['close']<p:
                # printred('止损赔钱:'+str(row[1]['close']-p))
                # sum = sum + row[1]['close']
                # have = False
                pass

    if have:
        sum = sum + row[1]['close']
    return sum



def oneshare_oneday_run(code,date = '2020-08-17'):
    dw = get_share(code,date)
    return run(dw)

# oneshare_oneday_run('128052')


def shares_oneday_run(codes,date = '2020-08-17'):
    income = []
    for i in codes:
        incomdata = oneshare_oneday_run(i,date)
        income.append(incomdata)
    return pd.DataFrame({'code':codes, 'income':income})


# dates = ['2020-08-'+str(i) for i in range(17,22)] 
# codes = ['123017','123018','123037','127004','128022','128043','110044','123014','128052','128041']
def shares_days_run(dates,codes):
    for i in dates:
        print('#'*10,i)
        df = shares_oneday_run(codes,i)
        print(df)
        print(df['income'].sum())

