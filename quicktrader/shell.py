import sys, os, logging

from quicktrader import clientConfig

def check_python():
    """
    检查python版本，打印提示信息
    :return
    """
    if sys.version_info <= (3, 5):
        raise TypeError("不支持 Python3.0 及以下版本，请升级")


def get_configByPath(config_path):
    find_config(config_path)



def find_config(config_path):
    if os.path.exists(config_path):
        return config_path
    config_path = os.path.join(os.path.dirname(__file__), config_path)
    if os.path.exists(config_path):
        return config_path
    raise TypeError("未找到配置文件")



def get_config(securitiesCompany,
        user,
        password,
        comm_password,
        exe_path,
        logLeve):
    logging.basicConfig(filename="log",
                        level=logLeve,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    config = {'sc':securitiesCompany,
                'user':user,
                'password':password,
                'comm_password':comm_password,
                'exe_path':exe_path}
    return config