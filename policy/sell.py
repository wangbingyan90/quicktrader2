

# 1，or (date.macd<0 and not date.kdjcrossintend) 小于零时,出场预测 
def run(date):
    # return comment(date)
    return date['kdjcross'] == -1 or (date.macd<0 and not date.kdjcrossintend) 
    


def comment(date):
    return date['kdjcross'] == -1 

def chareful(date):
    return date['kintend'] < 0 