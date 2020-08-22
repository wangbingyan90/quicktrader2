# -*- coding: utf-8 -*-
def create(broker):
    if broker == "yh":
        return YH
    if broker == "ht":
        return HT
    if broker == "gj":
        return GJ
    if broker == "ths":
        return CommonConfig
    if broker == "wk":
        return WK
    if broker == "htzq":
        return HTZQ()
    raise NotImplementedError


class CommonConfig:

    title = "网上股票交易系统5.0"

    top_window_className = "#32770" #顶层窗口类名

    capital_controlid = {
        "资金余额": 1012,
        "冻结资金": 1013,
        "可用金额": 1016,
        "可取金额": 1017,
        "总资产": 1015
    }

    
    optional = {}

    def __init__(self,opt):
        self.optional = opt


def HTZQ():
    opt = {
        'leftMenus':["AfxMDIFrame42s","SysTreeView32"],
        'rightMenus':["AfxMDIFrame42s","#32770"],
        'login':{
            "Edit1":'user',
            "Edit2":'password',
            "Edit3":'comm_password'
        },
        "buy":{
            'security':1032, 
            'amount':1034
        }
    }
    return CommonConfig(opt)
    # 'price':1033,


class YH(CommonConfig):
    DEFAULT_EXE_PATH = r"C:\双子星-中国银河证券\Binarystar.exe"

    BALANCE_GRID_CONTROL_ID = 1308

    GRID_DTYPE = {
        "操作日期": str,
        "委托编号": str,
        "申请编号": str,
        "合同编号": str,
        "证券代码": str,
        "股东代码": str,
        "资金帐号": str,
        "资金帐户": str,
        "发生日期": str,
    }

    AUTO_IPO_MENU_PATH = ["新股申购", "一键打新"]


class HT(CommonConfig):
    DEFAULT_EXE_PATH = r"C:\htzqzyb2\xiadan.exe"

    BALANCE_CONTROL_ID_GROUP = {
        "资金余额": 1012,
        "冻结资金": 1013,
        "可用金额": 1016,
        "可取金额": 1017,
        "股票市值": 1014,
        "总资产": 1015,
    }

    GRID_DTYPE = {
        "操作日期": str,
        "委托编号": str,
        "申请编号": str,
        "合同编号": str,
        "证券代码": str,
        "股东代码": str,
        "资金帐号": str,
        "资金帐户": str,
        "发生日期": str,
    }

    AUTO_IPO_MENU_PATH = ["新股申购", "批量新股申购"]


class GJ(CommonConfig):
    DEFAULT_EXE_PATH = "C:\\全能行证券交易终端\\xiadan.exe"

    GRID_DTYPE = {
        "操作日期": str,
        "委托编号": str,
        "申请编号": str,
        "合同编号": str,
        "证券代码": str,
        "股东代码": str,
        "资金帐号": str,
        "资金帐户": str,
        "发生日期": str,
    }

    AUTO_IPO_MENU_PATH = ["新股申购", "新股批量申购"]


class WK(HT):
    pass
