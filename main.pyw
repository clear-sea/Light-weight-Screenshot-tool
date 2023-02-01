import tkinter as tk
from pynput import keyboard
import time
from PIL import Image,ImageGrab,ImageTk
import json
import os
import datetime
import threading
import cv2
import numpy as np

#创建并且初始化全局变量
image=None
start_x=start_y=end_x=end_y=0
frames=[]
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
    main_window.geometry("400x100")
    main_window.iconbitmap("images/icon.ico")
    main_window.resizable(False,False)
    main_window.title("LightScreenShot")

    #gui界面
    #全屏按钮
    btn1=tk.Button(main_window,bg="white",text="全屏截图",cursor="hand2",command=full_screenshot)
    btn1.place(x=0,y=0,width=100,height=100)
    #矩形按钮
    btn2=tk.Button(main_window,bg="white",text="矩形截图",cursor="hand2",command=rect_screenshot)
    btn2.place(x=100,y=0,width=100,height=100)
    #GIF按钮
    btn3=tk.Button(main_window,bg="white",text="GIF截图",cursor="hand2",command=make_GIF)
    btn3.place(x=200,y=0,width=100,height=100)

    main_window.mainloop()

    main_window=None

#其他功能函数
def create_dirs(path):
    if not os.path.exists(path):
        os.mkdir(path)

def success_msg(mode,file_path):
    '''
        image:PIL Image type;
        mode:"image","gif","video"
    '''
    if main_window==None:
        msg=tk.Tk()
    else:
        msg=tk.Toplevel(main_window)
    
    screen_size=(msg.winfo_screenwidth(),msg.winfo_screenheight())
    msg.geometry(f"200x70+{screen_size[0]-200}+{screen_size[1]-70}")

    msg.attributes("-alpha",1.0)
    msg.attributes("-topmost",True)
    msg.overrideredirect(True)

    def close(event):
        msg.destroy()

    def open_image(event):
        Image.open(file_path).show()

    msg.bind("<Button-1>",close)

    if mode=="image":
        info="截图成功(左键单击关闭)"
    elif mode=="gif":
        info="录制GIF结束(左键单击关闭)"
    elif mode=="video":
        info="录制视频结束(左键单击关闭)"
    else:
        info=None

    t0=tk.Label(msg,text=info,font=("宋体",10))
    t0.place(x=0,y=0,width=200,height=35)
    t1=tk.Label(msg,text=f"已保存在:\n{file_path}\n点击打开",font=("宋体",10,"underline"))
    t1.place(x=0,y=35,width=200,height=35)

    t1.bind("<Button-1>",open_image)

    msg.mainloop()

#功能函数
#0全屏截图函数
def full_screenshot():
    print("[DEBUG]全屏截图")
    global image

    image=ImageGrab.grab()
    create_dirs(settings["save-path"])
    file_path=settings["save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".jpg"
    image.save(file_path)
    
    success_msg("image",file_path)
#1画出矩形区域截图函数
def rect_screenshot():
    print("[DEBUG]矩形截图")
    global image,start_x,start_y,end_x,end_y,main_window,rect_thread

    image=ImageGrab.grab()#先截取全屏幕
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
        global start_x,start_y,end_x,end_y,image

        fsc_window.destroy()

        if not((end_x-start_x==0)and(end_y-start_y==0)):
            if not((end_x<start_x)or(end_y<start_y)):
                image=image.crop((start_x,start_y,end_x,end_y))#再把全屏截图截取指定部分
                
                create_dirs(settings["save-path"])
                file_path=settings["save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".jpg"
                image.save(file_path)
                
                success_msg("image",file_path)

        start_x=start_y=end_x=end_y=0

    def start(event):
        global start_x,start_y,end_x,end_y

        start_x,start_y=event.x,event.y

    def OnDrag(event):
        global start_x,start_y,end_x,end_y

        end_x=event.x
        end_y=event.y
        cv.delete("all")
        cv.create_rectangle(start_x,start_y,end_x-start_x,end_y-start_y,fill="black")

    fsc_window.bind("<ButtonRelease-1>",grab)
    fsc_window.bind("<Button-1>",start)
    fsc_window.bind("<B1-Motion>",OnDrag)
    fsc_window.bind("<Escape>",lambda event:fsc_window.destroy())

    fsc_window.mainloop()
    rect_thread=threading.Thread(target=rect_screenshot)
#2 GIF录制函数
def make_GIF():
    global is_doing,frames,GIF_thread
    is_doing=True
    '''
    生成录制视频函数
    :return:
    '''
    file_path=settings["save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".gif"

    print("[DEBUG]开始录制GIF")
    #开始录制
    while True:
        img = ImageGrab.grab()
        frames.append(img)

        if is_doing==False:
            print('[DEBUG]屏幕录制GIF已经结束')
            frames[0].save(file_path,save_all=True,loop=True,append_images=frames[1:],duration=100)
            break

    success_msg("gif",file_path)
    GIF_thread=threading.Thread(target=make_GIF)

def stop_GIF():
    global is_doing
    is_doing=False
    return False

#3 录制视频
def make_video():
    global is_doing,video_thread
    is_doing=True
    '''
    生成录制视频函数
    :return:
    '''
    file_path=settings["save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    screen = ImageGrab.grab()
    width, height = screen.size
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(f'{file_path}.mp4', fourcc, 20, (width, height))

    print("[DEBUG]开始录制")
    #开始录制
    while True:
        im1 = ImageGrab.grab()
        im2 = cv2.cvtColor(np.array(im1), cv2.COLOR_RGB2BGR)
        video.write(im2)
        if is_doing==False:
            print('[DEBUG]屏幕录制已经结束')
            break
    video.release()
    success_msg("video",file_path)

    video_thread=threading.Thread(target=make_video)

def stop_video():
    global is_doing
    is_doing=False
    return False

def listen_key(key):
    global PrtScr,Ctrl,Shift,video_thread,GIF_thread,rect_thread
    #特殊按键监听
    if key==keyboard.Key.print_screen:
        print("[DEBUG]按下PrintScreen")
        PrtScr=True
    if key==keyboard.Key.ctrl or key==keyboard.Key.ctrl_r or key==keyboard.Key.ctrl_l:
        print("[DEBUG]按下Ctrl")
        Ctrl=True
    if key==keyboard.Key.shift or key==keyboard.Key.shift_r or key==keyboard.Key.shift_l:
        print("[DEBUG]按下Shift")
        Shift=True
    #如果按下组合键
    if PrtScr and Ctrl==False and Shift ==False:
        PrtScr=False
        full_screenshot()
    elif PrtScr==True and Ctrl==True and Shift==False:
        PrtScr=False
        Ctrl=False
        rect_thread.start()
    elif PrtScr==True and Shift==True and Ctrl==False and is_doing==False:
        PrtScr=False
        Shift=False
        video_thread.start()

    elif PrtScr==True and Shift==True and Ctrl==False and is_doing==True:
        PrtScr=False
        Shift=False
        stop_video()

    elif PrtScr and Shift and Ctrl and is_doing==False:
        PrtScr=False
        Shift=False
        Ctrl=False
        GIF_thread.start()

    elif PrtScr and Shift and Ctrl and is_doing:
        stop_GIF()

#全局键盘事件监听
if __name__=="__main__":
    gui_thread = threading.Thread(target=show_GUI)
    video_thread=threading.Thread(target=make_video)
    GIF_thread=threading.Thread(target=make_GIF)
    rect_thread=threading.Thread(target=rect_screenshot)
    gui_thread.start()
    #监听键盘
    with keyboard.Listener(on_press=listen_key) as listener:
        listener.join()

