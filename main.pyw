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

#导入之后执行的任务
#读取配置文件
with open("settings.json","r",encoding="utf-8") as f:
    settings=json.load(f)

#显示gui界面函数
def show_GUI():
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
    btn3=tk.Button(main_window,bg="white",text="GIF截图",cursor="hand2",command=GIF_screenshot)
    btn3.place(x=200,y=0,width=100,height=100)

    main_window.mainloop()

#其他功能函数
def create_dirs(path):
    if not os.path.exists(path):
        os.mkdir(path)

def success_msg(mode,file_path):
    '''
        image:PIL Image type;
        mode:"image","gif","video"
    '''
    msg=tk.Tk()
    
    screen_size=(msg.winfo_screenwidth(),msg.winfo_screenheight())
    msg.geometry(f"250x50+{screen_size[0]-250}+{screen_size[1]-50}")

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
    t0.place(x=0,y=0,width=200,height=25)
    t1=tk.Label(msg,text=f"已保存在:\n{file_path}\n点击打开",font=("宋体",7,"underline"))
    t1.place(x=0,y=25,width=200,height=25)
    t2=tk.Label(msg,image=ImageTk.PhotoImage(Image.open(file_path).resize((50,50))))
    t2.place(x=200,y=0,width=50,height=50)

    t1.bind("<Button-1>",open_image)

def save(image,mode=settings["image-save-mode"]):
    if mode=="file-save":
        create_dirs(settings["image-save-path"])
        file_path=settings["image-save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".jpg"
        image.save(file_path)
        
        success_msg("image",file_path)

#功能函数
#全局变量
image=None
start_x=start_y=end_x=end_y=0
frames=[]
is_doing=False
GIF_threading=None
#0全屏截图函数
def full_screenshot():
    global image

    image=ImageGrab.grab()
    save(image)
#1画出矩形区域截图函数
def rect_screenshot():
    global image,start_x,start_y,end_x,end_y

    image=ImageGrab.grab()#先截取全屏幕
    #初始化
    fsc_window=tk.Tk()
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
                
                save(image)

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
#2 GIF录制函数
def GIF_begin(self):
    global frames

    while True:
        if is_doing:
            frames.append(ImageGrab.grab((start_x,start_y,end_x,end_y)))
            time.sleep(1/24)
        elif is_doing==False:
            break

    create_dirs(settings["image-save-path"])
    file_path=settings["image-save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".gif"
    frames[0].save(file_path,append_images=frames[1:],save_all=True,loop=True)
    success_msg("gif",file_path)

def GIF_screenshot(mode=settings["gif-save-mode"]):
    global frames,is_doing,GIF_threading
    #初始化
    fsc_window=tk.Tk()
    fsc_window.attributes("-alpha",0.6)
    fsc_window.attributes("-topmost",True)
    fsc_window.attributes("-fullscreen",True)

    cv=tk.Canvas(fsc_window,bg="white")
    cv.place(x=0,y=0,width=fsc_window.winfo_screenwidth(),height=fsc_window.winfo_screenheight())

    def start(event):
        global start_x,start_y,end_x,end_y

        #结束划定区域，开始录GIF
        fsc_window.destroy()
        GIF_threading=threading.Thread(target=GIF_begin)
        GIF_threading.start()
        #创建并且初始化工具条窗口
        tool_bar=tk.Tk()
        tool_bar.geometry(f"100x25+{tool_bar.winfo_screenwidth()-100}+{int(tool_bar.winfo_screenheight()/2)}")
        tool_bar.attributes("-topmost",True)
        tool_bar.overrideredirect(True)

        def stop_GIF():
            global is_doing

            is_doing=False
        
        b1=tk.Button(tool_bar,text="stop",command=stop_GIF)
        b2=tk.Button(tool_bar,text="exit",command=lambda:tool_bar.destroy())
        b1.place(x=0,y=0,width=50,height=25)
        b2.place(x=50,y=0,width=50,height=25)
        #开始录屏GIF
        if not((end_x-start_x==0)and(end_y-start_y==0)):
            if end_x<start_x:
                start_x,end_x=end_x,start_x
            elif end_y<start_y:
                start_y,end_y=end_y,start_y


        start_x=start_y=end_x=end_y=0

    def press(event):
        global start_x,start_y,end_x,end_y
        #按下左键开始划定区域
        start_x,start_y=event.x,event.y

    def OnDrag(event):
        global start_x,start_y,end_x,end_y

        #正在拖拽
        end_x=event.x
        end_y=event.y
        cv.delete("all")
        cv.create_rectangle(start_x,start_y,end_x-start_x,end_y-start_y,fill="black")

    fsc_window.bind("<ButtonRelease-1>",start)
    fsc_window.bind("<Button-1>",press)
    fsc_window.bind("<B1-Motion>",OnDrag)
    fsc_window.bind("<Escape>",lambda event:fsc_window.destroy())

#3 录制视频
def make_video():
    global is_doing
    is_doing=True
    '''
    生成录制视频函数
    :return:
    '''
    file_name = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    screen = ImageGrab.grab()
    width, height = screen.size
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter('%s.avi' % file_name, fourcc, 20, (width, height))
    for n in range(3):
        print(str(3 - n) + '秒后开始录制！')
        time.sleep(1)
    while True:
        im1 = ImageGrab.grab()
        im2 = cv2.cvtColor(np.array(im1), cv2.COLOR_RGB2BGR)
        video.write(im2)
        if is_doing==False:
            print('屏幕录制已经结束')
            break
    video.release()

def stop_video(key):
    '''
    键盘监听函数
    :param key:
    :return:
    '''
    global is_doing
    if key == keyboard.Key.esc:
        print('结束录制')
        is_doing=False
        return False

#全局键盘事件监听
if __name__=="__main__":
    thread_ = threading.Thread(target=make_video)
    thread_.start()
    print(' 开始视频录制')
    with keyboard.Listener(on_press=stop_video) as listener:
        listener.join()

