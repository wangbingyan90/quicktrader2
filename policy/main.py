import meshare, algorithm,buy,sell
from colorama import init,Fore
import pandas as pd
init(autoreset=True)

pri = False
def prints(str):
    global pri
    if pri:
        print(str)
    pass

def printme(date,str1):
    if date['kdj'] > 0:
        if date['macd'] > 0:
            if date['macdintend'] > 0:
                prints(Fore.RED+str1)
            else:
                prints(Fore.MAGENTA+str1)
        else:                                            
            if date['macdintend'] > 0:
                prints(Fore.GREEN+str1)
            else:
                prints(Fore.YELLOW+str1)
    else:
        prints(str1)


def get_share(code,date = '2020-08-21'):
    # dw = meshare.get_today_min_data_bytick(code)
    dw = meshare.get_day_min_data_bytick(code,date)
    dw = algorithm.calc_kdj(dw)
    dw = algorithm.calc_macd(dw)
    return dw


def run(dw):
    infailcount = 0
    count = 0
    muncount = 0
    failcount = 0
    have = False
    sum = 0
    p = 0

    open = dw.loc[0].close

    for i in range(len(dw)):

        date = dw.loc[i]

        str1 = str(date.day)+'_'*5+str(date.close)[:5]+'_'*5+'dif:'+str(date.dif)[:6]+'_'*5+'macd:'+str(date.macd)[:4]+'_'*5+'k:'+str(date.k)[:4]+'_'*5+'Kdj:'+str(date.kdj)[:4]+'_'*5+'kdjcrossintend:'+str(date.kdjcrossintend)[:4]
        printme(date,str1)

        if not have:
            # 买入策略
            if buy.run(date):
                # if dw.loc[i+1]['close'] < date['close']:
                #     infailcount = infailcount + 1
                muncount = muncount + 1
                prints('买入')
                p = date['close']
                sum = sum - date['close']
                have = True
        else:
            # 卖出策略
            
            if sell.run(date):
                if dw.loc[i-1]['close'] > date['close']:
                    count = count + 1

                if date['close']<p:
                    prints('赔钱:'+str(date['close']-p))
                    failcount = failcount + 1
                else:
                    prints('卖出:'+str(date['close']-p))
                sum = sum + date['close']

                have = False

    if have:
        sum = sum + date['close']
    # print('_'*10)
    # print('总交易次数'+str(muncount))
    # print('买晚交易次数'+str(count))
    # print('失败交易次数'+str(failcount))
    # print('入场失败交易次数'+str(infailcount))
    return sum, dw.loc[i].close-open


def oneshare_oneday_run(code,date = '2020-08-17'):
    dw = get_share(code,date)
    return run(dw)



def oneshare_days_run(code,dates):
    income = []
    realincome = []
    for i in dates:
        incomdata,realincomedata = oneshare_oneday_run(code,i)
        income.append(incomdata)
        realincome.append(realincomedata)
        # print(i,'____',incomdata)
    
    return pd.DataFrame({'day':dates, 'income':income,'realincome':realincome})



def shares_oneday_run(codes,date = '2020-08-17'):
    income = []
    for i in codes:
        incomdata = oneshare_oneday_run(i,date)
        income.append(incomdata)
        # print(i,'____',incomdata)
    return pd.DataFrame({'code':codes, 'income':income})



def shares_days_run(codes,dates):
    global pri
    if len(codes)==1:
        pri = True
    dw = pd.DataFrame({'day':dates})
    coder = []
    for code in codes:
        # print(code)
        d = oneshare_days_run(code,dates)
        dw[code] = d['income']
        dw[code+'r'] = d['realincome']
        coder.append(code+'r')
    
    sum = dw[codes+coder].sum()
    sincome = sum[codes].sum()
    rincome = sum[coder].sum()
    sum["day"]="Summary"
    dw = dw.append(sum,ignore_index=True)
    print(dw)
    print(sincome)
    print(rincome)
    
codes = ['123018']
dates = ['2020-08-24']
# codes = ['123017','123018','123037','127004','128022']
# codes = ['123017','123018','123037','127004','128022','128043','110044','123014','128052','128041']
# dates = ['2020-08-'+str(i) for i in range(17,22)] 
# codes = ['127004','110044','123015','123013','128112','128073','123041','128041','123037','123014']
shares_days_run(codes,dates)


