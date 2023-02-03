import tkinter as tk#图形界面 内置库
from tkinter import messagebox#消息弹窗模块
from pynput import keyboard#键盘监听 第三方库
from PIL import Image,ImageGrab#PIL图像处理 第三方库
import json#json文件解析 内置库
import os#文件操作 内置库
import datetime#获取日期时间 内置库
import threading#多线程 内置库
import cv2#pyopencv2图像处理第三方库，用于合成视频 第三方库
import numpy as np#高级数学库，用于转换图像 第三方库
import pystray#windows系统托盘 第三方库
import win32clipboard
from io import BytesIO
import UI

#创建并且初始化全局变量
start_x=start_y=end_x=end_y=0
is_doing=False
main_window=None

PrtScr=False
Ctrl=False
Shift=False
#读取配置文件
with open("settings.json","r",encoding="utf-8") as f:
    settings=json.load(f)

#显示gui界面函数
def show_GUI():
    global main_window

    main_window=tk.Tk()
    main_window["bg"]="white"
    main_window.geometry("400x150")
    main_window.iconbitmap("images/icon.ico")
    main_window.resizable(False,False)
    main_window.title("LightScreenShot")
    main_window.protocol("WM_DELETE_WINDOW",main_window.withdraw)

    #gui界面
    #文本标签
    #0全屏文本
    l1=tk.Label(main_window,bg="white",text="全屏截图\nPrtScr")
    l1.place(x=0,y=0,width=100,height=100)
    #1矩形文本
    l2=tk.Label(main_window,bg="white",text="矩形截图\n(按esc退出)\nCtrl+PrtScr")
    l2.place(x=100,y=0,width=100,height=100)
    #2GIF文本
    l3=tk.Label(main_window,bg="white",text="开始/结束\nGIF录制\nCtrl+Shift+PrtScr")
    l3.place(x=200,y=0,width=100,height=100)
    #3视频录制文本
    l4=tk.Label(main_window,bg="white",text="开始/结束\n视频录制\nShift+PrtScr")
    l4.place(x=300,y=0,width=100,height=100)
    #按钮
    #0
    btn1=UI.Button(main_window,(10,110),(55,30),"设置",config)
    
    #主循环
    main_window.mainloop()

#功能函数
#0全屏截图函数
def full_screenshot():
    global icon

    image=ImageGrab.grab()
    file_path=settings["save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".jpg"
    image.save(file_path)
    
    icon.notify(f"截图成功\n已保存{file_path}","轻量截图")
#1画出矩形区域截图函数
def rect_screenshot():
    global start_x,start_y,end_x,end_y,main_window,icon

    all_image=ImageGrab.grab()#先截取全屏幕
    #初始化
    fsc_window=UI.Drag_Window(main_window)
    def grab(event):
        start_x=fsc_window.start_x
        start_y=fsc_window.start_y
        end_x=fsc_window.end_x
        end_y=fsc_window.end_y

        fsc_window.destroy()

        image=all_image.crop((start_x,start_y,end_x,end_y))#再把全屏截图截取指定部分
        #保存模式
        if settings["image-save-mode"]=="file":
            file_path=settings["save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".jpg"
            image.save(file_path)
            
            icon.notify(f"截图成功\n已保存{file_path}","轻量截图")
        elif settings["image-save-mode"]=="clipoard":
            output = BytesIO()
            # 用BMP (Bitmap) 格式存储
            # 这里是位图，然后用output字节对象来存储
            image.save(output, 'BMP')
            # BMP图片有14字节的header，需要额外去除
            data = output.getvalue()[14:]
            # 关闭
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB,data)
            win32clipboard.CloseClipboard()

            icon.notify(f"截图成功\n已储存到剪切板","轻量截图")

    fsc_window.bind("<ButtonRelease-1>",grab)
    fsc_window.bind("<Escape>",lambda event:fsc_window.destroy())

    start_x=start_y=end_x=end_y=None

#2 GIF录制函数
def make_GIF():
    global is_doing,icon,start_x,start_y,end_x,end_y
    if settings["get-area"]:
        #初始化
        fsc_window=UI.Drag_Window(main_window)
        #截取屏幕区域
        def grab(event):
            global start_x,start_y,end_x,end_y
            start_x=fsc_window.start_x
            start_y=fsc_window.start_y
            end_x=fsc_window.end_x
            end_y=fsc_window.end_y

            fsc_window.destroy()

        fsc_window.bind("<ButtonRelease-1>",grab)
        fsc_window.bind("<Escape>",lambda event:fsc_window.destroy())
        #end
    file_path=settings["save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".gif"

    icon.notify("开始录制GIF","轻量截图-录制GIF")
    #开始录制
    frames=[]
    while True:
        img = ImageGrab.grab((start_x,start_y,end_x,end_y))
        frames.append(img)

        if is_doing==False:
            icon.notify(f"录制GIF已结束\n已保存{file_path}","轻量截图-录制GIF")
            frames[0].save(file_path,save_all=True,loop=True,append_images=frames[1:],duration=100)
            break

    icon.notify(f"截图成功\n已保存{file_path}","轻量截图")
    start_x=start_y=end_x=end_y=0

#3 录制视频
def make_video():
    global is_doing,icon,start_x,start_y,end_x,end_y
    
    if settings["get-area"]:
        #初始化
        fsc_window=UI.Drag_Window(main_window)
        #截取屏幕区域
        def grab(event):
            global start_x,start_y,end_x,end_y
            start_x=fsc_window.start_x
            start_y=fsc_window.start_y
            end_x=fsc_window.end_x
            end_y=fsc_window.end_y

            fsc_window.destroy()

        fsc_window.bind("<ButtonRelease-1>",grab)
        fsc_window.bind("<Escape>",lambda event:fsc_window.destroy())
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

#按下按键
def listen_key_press(key):
    global PrtScr,Ctrl,Shift
    #特殊按键监听
    if key==keyboard.Key.print_screen:
        PrtScr=True
    if key==keyboard.Key.ctrl or key==keyboard.Key.ctrl_r or key==keyboard.Key.ctrl_l:
        Ctrl=True
    if key==keyboard.Key.shift or key==keyboard.Key.shift_r or key==keyboard.Key.shift_l:
        Shift=True
    #如果按下组合键
    if PrtScr and Ctrl==False and Shift==False:
        full_screenshot()
    elif PrtScr and Ctrl and Shift==False:
        start_rect_screenshot()
        
    elif PrtScr and Shift and Ctrl==False and is_doing==False:
        start_video()

    elif PrtScr and Shift and Ctrl==False and is_doing:
        stop_video_or_GIF()#结束视频录制

    elif PrtScr and Shift and Ctrl and is_doing==False:
        PrtScr=False
        Shift=False
        Ctrl=False
        start_GIF()

    elif PrtScr and Shift and Ctrl and is_doing:
        stop_video_or_GIF()#结束GIF
#松开按键
def listen_key_release(key):
    global PrtScr,Ctrl,Shift
    if key==keyboard.Key.print_screen:
        PrtScr=True
    if key==keyboard.Key.ctrl or key==keyboard.Key.ctrl_r or key==keyboard.Key.ctrl_l:
        Ctrl=True
    if key==keyboard.Key.shift or key==keyboard.Key.shift_r or key==keyboard.Key.shift_l:
        Shift=True

'''其他功能函数'''
#如果存放截图的文件夹不存在就创建一个
def create_dirs(path):
    if not os.path.exists(path):
        os.mkdir(path)
#退出整个程序函数
def on_exit(icon):
    icon.stop()
    os._exit(0)#强制退出
#打开截图保存的文件夹
def open_image_dir():
    global settings
    os.system(f"start {settings['save-path']}")
#设置
def config():
    global main_window
    #创建并初始化窗口
    window=tk.Toplevel(main_window)
    window.geometry("400x400")
    window.resizable(False,False)
    window.attributes("-toolwindow",True)
    window.title("设置")
    pass
    
#键盘监听的函数
def key_listener():
    #监听键盘
    with keyboard.Listener(on_press=listen_key_press,on_release=listen_key_release) as listener:
        listener.join()
    '''
    with keyboard.GlobalHotKeys({"<print_screen>":full_screenshot,"<ctrl>+p":start_rect_screenshot,"<shift>+p":start_video,"<ctrl>+<shift>+p":start_GIF}) as x:
        x.join()
    '''
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
    menu0=pystray.MenuItem(text="🪟显示主窗口",action=main_window.deiconify)
    menu1=pystray.MenuItem(text="⚙️设置",action=config)
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
