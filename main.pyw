import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
from PIL import Image,ImageGrab
import json
import os
import datetime
import threading
import cv2
import numpy as np
import pystray

#创建并且初始化全局变量
start_x=start_y=end_x=end_y=0
is_doing=False
main_window=None
is_main_window_alive=False

PrtScr=False
Ctrl=False
Shift=False
#读取配置文件
with open("settings.json","r",encoding="utf-8") as f:
    settings=json.load(f)

#显示gui界面函数
def show_GUI():
    global main_window,is_main_window_alive

    if is_main_window_alive:
        return None

    main_window=tk.Tk()
    main_window.geometry("400x100")
    main_window.iconbitmap("images/icon.ico")
    main_window.resizable(False,False)
    main_window.title("LightScreenShot")
    main_window.protocol("WM_DELETE_WINDOW", )

    is_main_window_alive=True

    #gui界面
    #全屏
    l1=tk.Label(main_window,bg="white",text="全屏截图\nPrtScr")
    l1.place(x=0,y=0,width=100,height=100)
    #矩形
    l2=tk.Label(main_window,bg="white",text="矩形截图\n(按esc退出)\nCtrl+PrtScr")
    l2.place(x=100,y=0,width=100,height=100)
    #GIF
    l3=tk.Label(main_window,bg="white",text="开始/结束\nGIF录制\nCtrl+Shift+PrtScr")
    l3.place(x=200,y=0,width=100,height=100)
    #视频录制
    l4=tk.Label(main_window,bg="white",text="开始/结束\n视频录制\nShift+PrtScr")
    l4.place(x=300,y=0,width=100,height=100)
    main_window.mainloop()

    main_window=None

#其他功能函数
def create_dirs(path):
    if not os.path.exists(path):
        os.mkdir(path)
#画出屏幕的功能
def start(event):
        global start_x,start_y,end_x,end_y

        start_x,start_y=event.x,event.y

def OnDrag(event,cv):
    global start_x,start_y,end_x,end_y

    end_x=event.x
    end_y=event.y
    cv.delete("all")
    cv.create_rectangle(start_x,start_y,end_x-start_x,end_y-start_y,fill="black")
#功能函数
#0全屏截图函数
def full_screenshot():
    global icon

    image=ImageGrab.grab()
    create_dirs(settings["save-path"])
    file_path=settings["save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".jpg"
    image.save(file_path)
    
    icon.notify(f"截图成功\n已保存{file_path}","轻量截图")
#1画出矩形区域截图函数
def rect_screenshot():
    global start_x,start_y,end_x,end_y,main_window,icon

    all_image=ImageGrab.grab()#先截取全屏幕
    #初始化
    if main_window==None:
        fsc_window=tk.Tk()
    else:
        fsc_window=tk.Toplevel(main_window)

    fsc_window.attributes("-alpha",0.6)
    fsc_window.attributes("-topmost",True)
    fsc_window.attributes("-fullscreen",True)

    cv=tk.Canvas(fsc_window,bg="white")
    cv.place(x=0,y=0,width=fsc_window.winfo_screenwidth(),height=fsc_window.winfo_screenheight())

    def grab(event):
        fsc_window.destroy()

        if not((end_x-start_x==0)and(end_y-start_y==0)):
            if not((end_x<start_x)or(end_y<start_y)):
                image=all_image.crop((start_x,start_y,end_x,end_y))#再把全屏截图截取指定部分
                file_path=settings["save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".jpg"
                image.save(file_path)
                
                icon.notify(f"截图成功\n已保存{file_path}","轻量截图")

    fsc_window.bind("<ButtonRelease-1>",grab)
    fsc_window.bind("<Button-1>",start)
    fsc_window.bind("<B1-Motion>",lambda event:OnDrag(event,cv))
    fsc_window.bind("<Escape>",lambda event:fsc_window.destroy())

    if main_window==None:
        fsc_window.mainloop()

    start_x=start_y=end_x=end_y=0

#2 GIF录制函数
def make_GIF():
    global is_doing,icon,start_x,start_y,end_x,end_y
    
    #end
    file_path=settings["save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".gif"

    icon.notify("开始录制GIF","轻量截图-录制GIF")
    #开始录制
    frames=[]
    while True:
        img = ImageGrab.grab()
        frames.append(img)# (start_x,start_y,end_x,end_y)

        if is_doing==False:
            icon.notify(f"录制GIF已结束\n已保存{file_path}","轻量截图-录制GIF")
            frames[0].save(file_path,save_all=True,loop=True,append_images=frames[1:],duration=100)
            break

    icon.notify(f"截图成功\n已保存{file_path}","轻量截图")
    start_x=start_y=end_x=end_y=0

#3 录制视频
def make_video():
    global is_doing,icon,start_x,start_y,end_x,end_y
    #截取屏幕区域
    #初始化
    if main_window==None:
        fsc_window=tk.Tk()
    else:
        fsc_window=tk.Toplevel(main_window)

    fsc_window.attributes("-alpha",0.6)
    fsc_window.attributes("-topmost",True)
    fsc_window.attributes("-fullscreen",True)

    cv=tk.Canvas(fsc_window,bg="white")
    cv.place(x=0,y=0,width=fsc_window.winfo_screenwidth(),height=fsc_window.winfo_screenheight())

    def grab(event):
        global start_x,start_y,end_x,end_y

        fsc_window.destroy()

        if not((end_x-start_x==0)and(end_y-start_y==0)):
            if end_x<start_x:
                start_x,end_x=end_x,start_x
            if end_y<start_y:
                start_y,end_y=end_y,start_y

    fsc_window.bind("<ButtonRelease-1>",grab)
    fsc_window.bind("<Button-1>",start)
    fsc_window.bind("<B1-Motion>",lambda event:OnDrag(event,cv))
    fsc_window.bind("<Escape>",lambda event:fsc_window.destroy())

    if main_window==None:
        fsc_window.mainloop()
    #end
    file_path=settings["save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    screen = ImageGrab.grab((start_x,start_y,end_x,end_y))
    width, height = screen.size
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(f'{file_path}.mp4', fourcc, 20, (width, height))

    icon.notify("开始录制视频","轻量截图-录制视频")
    #开始录制
    while True:
        image = ImageGrab.grab((start_x,start_y,end_x,end_y))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        video.write(image)
        if is_doing==False:
            icon.notify(f"录制视频结束\n已保存在{file_path}","轻量截图-录制视频")
            start_x=start_y=end_x=end_y=0
            break
    video.release()

def stop_video_or_GIF():
    global is_doing,menu2
    menu2.__init__(text="⏹️停止",action=stop_video_or_GIF,enabled=False)
    is_doing=False

def start_rect_screenshot():
    #创建并启动矩形截图线程
    rect_thread=threading.Thread(target=rect_screenshot)
    rect_thread.start()
def start_video():
    global is_doing

    if is_doing==False:
        is_doing=True
        menu2.__init__(text="⏹️停止",action=stop_video_or_GIF,enabled=True)
        #创建并启动视频录制线程
        video_thread=threading.Thread(target=make_video)
        video_thread.start()
    else:
        messagebox.showwarning("轻量截图-警告","不能同时录制屏幕视频和录制GIF")
def start_GIF():
    global is_doing

    if is_doing==False:
        is_doing=True
        menu2.__init__(text="⏹️停止",action=stop_video_or_GIF,enabled=True)
        #创建并启动GIF线程
        GIF_thread=threading.Thread(target=make_GIF)
        GIF_thread.start()
    else:
        messagebox.showwarning("轻量截图-警告","不能同时录制屏幕视频和录制GIF")

def listen_key(key):
    global PrtScr,Ctrl,Shift
    #特殊按键监听
    if key==keyboard.Key.print_screen:
        PrtScr=True
    if key==keyboard.Key.ctrl or key==keyboard.Key.ctrl_r or key==keyboard.Key.ctrl_l:
        Ctrl=True
    if key==keyboard.Key.shift or key==keyboard.Key.shift_r or key==keyboard.Key.shift_l:
        Shift=True
    #如果按下组合键
    if PrtScr and Ctrl==False and Shift ==False:
        PrtScr=False
        full_screenshot()
    elif PrtScr==True and Ctrl==True and Shift==False:
        PrtScr=False
        Ctrl=False
        start_rect_screenshot()
        
    elif PrtScr==True and Shift==True and Ctrl==False and is_doing==False:
        PrtScr=False
        Shift=False
        start_video()

    elif PrtScr==True and Shift==True and Ctrl==False and is_doing==True:
        PrtScr=False
        Shift=False
        stop_video_or_GIF()#结束视频录制

    elif PrtScr and Shift and Ctrl and is_doing==False:
        PrtScr=False
        Shift=False
        Ctrl=False
        start_GIF()

    elif PrtScr and Shift and Ctrl and is_doing:
        stop_video_or_GIF()#结束GIF
#退出整个程序函数
def on_exit(icon):
    icon.stop()
    os._exit(0)#强制退出
#打开截图保存的文件夹
def open_image_dir():
    global settings
    os.system(f"start {settings['save-path']}")
#键盘监听的函数
def key_listener():
    #监听键盘
    with keyboard.Listener(on_press=listen_key) as listener:
        listener.join()
#全局键盘事件监听
if __name__=="__main__":
    create_dirs(settings["save-path"])
    gui_thread = threading.Thread(target=show_GUI)
    key_listener_thread=threading.Thread(target=key_listener)
    #显示界面
    gui_thread.start()
    #监听键盘
    key_listener_thread.start()
    #显示系统托盘
    icon_img=Image.open("images/icon.jpg")#图标
    #托盘菜单
    menu0=pystray.MenuItem(text="🪟显示主窗口",action=show_GUI)
    menu1=pystray.MenuItem(text="⚙️设置",action=None,enabled=False)
    menu2=pystray.MenuItem(text="⏹️停止",action=stop_video_or_GIF,enabled=False)
    menu3=pystray.MenuItem(text="全屏截图",action=full_screenshot)
    menu4=pystray.MenuItem(text="矩形截图",action=start_rect_screenshot)
    menu5=pystray.MenuItem(text="录制GIF",action=start_GIF)
    menu6=pystray.MenuItem(text="录制视频",action=start_video)
    menu7=pystray.MenuItem(text="📂打开截图文件夹",action=open_image_dir)
    menu8=pystray.MenuItem(text="❌退出",action=on_exit,default=True)
    
    menu=pystray.Menu(menu0,menu1,menu2,menu3,menu4,menu5,menu6,menu7,menu8)
    #显示托盘图标
    icon = pystray.Icon("轻量截图LightScreenShot", icon_img, "轻量截图\nLightSreenShot",menu)
    icon.run()
