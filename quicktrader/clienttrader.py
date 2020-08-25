import pywinauto, time

from quicktrader import clientConfig

class clienttrader():


    def __init__(self,config):
        self.config = config
        self.clconfig = clientConfig.create(self.config['sc'])


    def login(self):
        # TODO 已存在 链接的情况
        self.app = pywinauto.Application().start(self.config['exe_path'])
        self.app.Dlg.wait_not('active')

        
        for op, text in self.clconfig.optional['login'].items():
            self.edit_className(op,self.config[text])

        self.app.top_window().button0.click()

        # detect login is success or not
        self.app.top_window().wait_not("exists", 100)
        self.close_prompt_windows()

    
    def close_prompt_windows(self):
        for window in self.app.windows(
            class_name=self.clconfig.top_window_className,
            visible_only=True):

            title = window.window_text()
            if title != self.clconfig.title:
                window.close()
                time.sleep(0.2)
        self.main = self.app.top_window()


    def init(self):
        self.init_left_menus()


    def init_left_menus(self):
        for str1 in self.clconfig.optional["leftMenus"]:
            self.leftMenus = self.main.child_window(class_name=str1)
    

    def init_right_menus(self):
        for str1 in self.clconfig.optional["rightMenus"]:
            self.rightMenus = self.main.child_window(class_name=str1)


    def sell(self, security, price, amount):
        t = {'security':security, 'price':price, 'amount':amount}
        self.leftMenus.select("\\卖出[F2]")
        # self.main.child_window(control_id=1006, class_name="Button").wait('ready')
        # time.sleep(1) # TODO 目前没有更好的方法sell

        for name,id in self.clconfig.optional["buy"].items():
            self.edit_winid(id,t[name])
            
        # time.sleep(1)
        self.main.child_window(control_id=1006, class_name="Button").click()
        # time.sleep(2)
        self.app.top_window().child_window(control_id=1365).window_text() #委托确认
        self.app.top_window().child_window(class_name='Static',control_id = 1040).window_text()
        self.app.top_window().type_keys("%Y")
        # time.sleep(1)
        self.app.top_window().child_window(control_id=1365).window_text() #提示
        self.app.top_window().child_window(class_name='Static',control_id = 1004).window_text()
        self.app.top_window()["确定"].click()


    def buy(self, security, price, amount):
        t = {'security':security, 'price':price, 'amount':amount}
        
        self.leftMenus.select("\\买入[F1]")

        # self.main.child_window(control_id=1006, class_name="Button").wait('ready')
        # time.sleep(0.2) # TODO 目前没有更好的方法

        for name,id in self.clconfig.optional["buy"].items():
            self.edit_winid(id,t[name])

        # time.sleep(0.5)
        self.main.child_window(control_id=1006, class_name="Button").click()
        # time.sleep(0.5)
        self.app.top_window().child_window(control_id=1365).window_text() #委托确认
        # self.app.top_window().child_window(class_name='Static',control_id = 1040).window_text()
        self.app.top_window().type_keys("%Y")
        # time.sleep(0.5)
        self.app.top_window().child_window(control_id=1365).window_text() #提示
        # self.app.top_window().child_window(class_name='Static',control_id = 1004).window_text()
        self.app.top_window()["确定"].click()


    def edit_winid(self,control_id,text):
        self.main.child_window(control_id=control_id, class_name="Edit").set_focus()
        # print(text)
        self.main.child_window(control_id=control_id, class_name="Edit").set_edit_text(text)


    def edit_className(self,op,text):
        # self.app.top_window()[op].set_focus()
        self.app.top_window()[op].type_keys(text)

    code = '0000'
    haves = None
    # 查看股票实时价格
    def look(self,code,have):
        if have:
            if have != self.haves:
                self.leftMenus.select("\\卖出[F2]")
                time.sleep(0.5)
                self.main.child_window(control_id=1032, class_name="Edit").set_edit_text(code)
                self.code = code
                self.haves = have
        else:
            if have != self.haves:
                self.leftMenus.select("\\买入[F1]")
                time.sleep(0.5)
                self.main.child_window(control_id=1032, class_name="Edit").set_edit_text(code)
                self.code = code
                self.haves = have
        
        if self.code != code:
            self.main.child_window(control_id=1032, class_name="Edit").set_edit_text(code)
            self.code = code

        while '-' == self.main.child_window(control_id=1024, class_name="Static").window_text():
            pass
        return float(self.main.child_window(control_id=1024, class_name="Static").window_text())




def start(
    securitiesCompany = None,
    user=None,
    password=None,
    comm_password=None,
    exe_path=None,
    **kwargs):
    config = {'sc':securitiesCompany,
                'user':user,
                'password':password,
                'comm_password':comm_password,
                'exe_path':exe_path}
    user = clienttrader(config)
    user.login()
    user.init()

    return user





        



    