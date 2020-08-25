import tkinter 
import text
from tkinter import messagebox
class Login(object): 
 def __init__(self): 
  
  # 创建主窗口,用于容纳其它组件 
  self.root = tkinter.Tk() 
  # 给主窗口设置标题内容 
#   self.root.title("影视资源管理系统(离线版)"/) 
  self.root.geometry('450x300') 
  #运行代码时记得添加一个gif图片文件，不然是会出错的
#   self.canvas = tkinter.Canvas(self.root, height=200, width=500)#创建画布 
#   self.image_file = tkinter.PhotoImage(file='C:\\Users\\wby\\Pictures\\2.gif')#加载图片文件 
#   self.image = self.canvas.create_image(0,0, anchor='nw', image=self.image_file)#将图片置于画布上 
#   self.canvas.pack(side='top')#放置画布（为上端） 
  #创建一个`label`名为`Account: ` 
  
  self.run = tkinter.Button(self.root, text='启动',command = lambda : self.runf()) 

  self.sharee1 = tkinter.Entry(self.root, width=30) 
  self.shareb1 = tkinter.Button(self.root, text='买',command = lambda : self.buy(self.sharee1.get())) 
  self.shares1 = tkinter.Button(self.root, text='卖',command = lambda : self.sel(self.sharee1.get())) 

  self.sharee2 = tkinter.Entry(self.root, width=30) 
  self.shares2 = tkinter.Button(self.root, text='卖',command = lambda : self.sel(self.sharee2.get()))
  self.shareb2 = tkinter.Button(self.root, text='买',command = lambda : self.buy(self.sharee2.get())) 


  self.sharee3 = tkinter.Entry(self.root, width=30) 
  self.shareb3 = tkinter.Button(self.root, text='买',command = lambda : self.buy(self.sharee3.get())) 
  self.shares3 = tkinter.Button(self.root, text='卖',command = lambda : self.sel(self.sharee3.get())) 

  self.sharee2 = tkinter.Entry(self.root, width=30) 
  self.shares2 = tkinter.Button(self.root, text='卖',command = lambda : self.sel(self.sharee2.get()))
  self.shareb2 = tkinter.Button(self.root, text='买',command = lambda : self.buy(self.sharee2.get())) 
  # 完成布局 
 def gui_arrang(self): 
  self.run.place(x=170, y= 20)
  
  self.shareb1.place(x=20, y= 70)
  self.shares1.place(x=350, y=70) 
  self.sharee1.place(x=70, y=70) 
  self.shareb2.place(x=50, y= 120)
  self.shares2.place(x=350, y=120) 
  self.sharee2.place(x=100, y=120) 
  self.shareb3.place(x=50, y= 170)
  self.shares3.place(x=350, y=170) 
  self.sharee3.place(x=100, y=170) 
 
 def runf(self):
  self.c = text.getUser()

 # 进入注册界面 
 def buy(self,x):
  self.c.buy(x,x,x) 
  print(x)


 def sel(self,x): 
  self.c.sell(x,x,x) 

def main(): 
 # 初始化对象 
 L = Login() 
 # 进行布局 
 L.gui_arrang() 
 # 主程序执行 
 tkinter.mainloop() 
if __name__ == '__main__': 
 main()