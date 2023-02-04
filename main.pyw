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

is_GIF_running=False
is_video_running=False
is_collecting=False

main_window=None
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
    labels_frame=tk.Frame(main_window,bg="white")
    labels_frame.place(x=0,y=0,width=400,height=100)
    btns_frame=tk.Frame(main_window,bg="white")
    btns_frame.place(x=5,y=105,width=390,height=40)
    #文本标签
    #0全屏文本
    l1=tk.Label(labels_frame,bg="white",text="全屏截图\nCtrl+0")
    l1.place(x=0,y=0,width=100,height=100)
    #1矩形文本
    l2=tk.Label(labels_frame,bg="white",text="矩形截图\n(按esc退出)\nCtrl+p")
    l2.place(x=100,y=0,width=100,height=100)
    #2GIF文本
    l3=tk.Label(labels_frame,bg="white",text="开始/结束\nGIF录制\nCtrl+Alt")
    l3.place(x=200,y=0,width=100,height=100)
    #3视频录制文本
    l4=tk.Label(labels_frame,bg="white",text="开始/结束\n视频录制\nShift+Alt")
    l4.place(x=300,y=0,width=100,height=100)
    #按钮
    #0
    btn1=UI.Button(btns_frame,(0,0),(50,40),"设置",config)
    btn2=UI.Button(btns_frame,(60,0),(50,40),"关于",about)
    
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
    global start_x,start_y,end_x,end_y,main_window,icon,is_collecting

    if is_collecting==False:
        is_collecting=True#设置为正在截图

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
    else:
        pass

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
        if settings["get-area"]:
            img = ImageGrab.grab((start_x,start_y,end_x,end_y))
        else:
            img = ImageGrab.grab()
        frames.append(img)

        if is_GIF_running==False:
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
    if settings["get-area"]:
        screen = ImageGrab.grab((start_x,start_y,end_x,end_y))
    else:
        screen = ImageGrab.grab()
    width, height = screen.size
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(f'{file_path}.mp4', fourcc, 20, (width, height))

    icon.notify("开始录制视频","轻量截图-录制视频")
    #开始录制
    while True:
        if settings["get-area"]:
            image = ImageGrab.grab((start_x,start_y,end_x,end_y))
        else:
            image = ImageGrab.grab()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        video.write(image)
        if is_video_running==False:
            icon.notify(f"录制视频结束\n已保存在{file_path}","轻量截图-录制视频")
            start_x=start_y=end_x=end_y=0
            break
    video.release()

def stop_video():
    global is_video_running,menu2
    menu2.__init__(text="⏹️停止",action=stop_video,enabled=False)
    is_video_running=False

def stop_GIF():
    global is_GIF_running,menu2
    menu2.__init__(text="⏹️停止",action=stop_GIF,enabled=False)
    is_GIF_running=False

def start_rect_screenshot():
    #创建并启动矩形截图线程
    rect_thread=threading.Thread(target=rect_screenshot)
    rect_thread.start()
def start_video():
    global is_video_running

    if is_video_running==False:
        is_video_running=True
        menu2.__init__(text="⏹️停止",action=stop_video,enabled=True)
        #创建并启动视频录制线程
        video_thread=threading.Thread(target=make_video)
        video_thread.start()
    else:
        messagebox.showwarning("轻量截图-警告","正在录制视频")
def start_GIF():
    global is_GIF_running

    if is_GIF_running==False:
        is_GIF_running=True
        menu2.__init__(text="⏹️停止",action=stop_GIF,enabled=True)
        #创建并启动GIF线程
        GIF_thread=threading.Thread(target=make_GIF)
        GIF_thread.start()
    else:
        messagebox.showwarning("轻量截图-警告","正在录制GIF")

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
    global main_window,settings
    #创建并初始化窗口
    window=UI.Setting_Window(main_window,settings)
    pass
#关于
def about():
    global main_window
    window=UI.About_Window(main_window,"轻量截图，使用python语言，结合多个第三方库\n完整项目和详细说明链接地址：\n",(400,400),"关于")
    hyper_link=UI.HyperLink(window,"https://github.com/LightByteCode/LightScreenShot","https://github.com/LightByteCode/LightScreenShot",(0,100),(100,20),("宋体",10))
    
#键盘监听的函数
def key_listener():
    #监听键盘
    '''
    with keyboard.Listener(on_press=listen_key_press,on_release=listen_key_release) as listener:
        listener.join()
    ''' 
    with keyboard.GlobalHotKeys({"<ctrl>+0":full_screenshot,"<ctrl>+p":start_rect_screenshot,"<ctrl>+<alt>":start_GIF,"<shift>+<alt>":start_video}) as x:
        x.join()

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
    menu2=pystray.MenuItem(text="⏹️停止录屏",action=stop_video,enabled=False)
    menu3=pystray.MenuItem(text="⏹️停止录制GIF",action=stop_GIF,enabled=False)
    menu4=pystray.MenuItem(text="全屏截图",action=full_screenshot)
    menu5=pystray.MenuItem(text="矩形截图",action=start_rect_screenshot)
    menu6=pystray.MenuItem(text="录制GIF",action=start_GIF)
    menu7=pystray.MenuItem(text="录制视频",action=start_video)
    menu8=pystray.MenuItem(text="📂打开截图文件夹",action=open_image_dir)
    menu9=pystray.MenuItem(text="❌退出",action=on_exit,default=True)
    
    menu=pystray.Menu(menu0,menu1,menu2,menu3,menu4,menu5,menu6,menu7,menu8,menu9)
    #显示托盘图标
    icon = pystray.Icon("轻量截图LightScreenShot", icon_img, "轻量截图\nLightSreenShot",menu)
    icon.run()
