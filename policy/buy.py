
    


def comment(date):
    return date['kdjcross'] == 1

def chareful(date):
    return date['macdcross'] == 1
    
def run(date):
    return comment(date)
    # return chareful(date)
    # return date['difcross'] == 1