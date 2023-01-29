import time
from PIL import Image,ImageGrab,ImageTk
import json
import os
import datetime
import tkinter as tk
import threading

#导入之后执行的任务
#读取配置文件
with open("settings.json","r",encoding="utf-8") as f:
    settings=json.load(f)
#读取所需的图片文件
start_end_img=Image.open("images/start_end.png")
close_img=Image.open("images/close.png")
    
def create_dirs(path):
    if not os.path.exists(path):
        os.mkdir(path)

def success_msg(main_window,mode,file_path):
    '''
        image:PIL Image type;
        mode:"image","gif","video"
    '''
    alpha=1.0
    msg=tk.Toplevel(main_window)
    
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

def save(main_window,image,mode=settings["image-save-mode"]):
    if mode=="file-save":
        create_dirs(settings["image-save-path"])
        file_path=settings["image-save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".jpg"
        image.save(file_path)
        
        success_msg(main_window,"image",file_path)

class ScreenShot:
    def __init__(self):
        self.image=None 
        self.start_x=self.start_y=self.end_x=self.end_y=0 
        self.frames=[]
        self.GIF_thread=threading.Thread(target=self.GIF_begin)

    def full_screenshot(self,main_window):
        main_window.attributes("-alpha",0)
        self.image=ImageGrab.grab()
        main_window.attributes("-alpha",1)
        save(main_window,self.image)

    def rect_screenshot(self,main_window):
        main_window.attributes("-alpha",0)#主窗口隐藏
        self.image=ImageGrab.grab()#先截取全屏幕
        #初始化
        fsc_window=tk.Toplevel(main_window)
        fsc_window.attributes("-alpha",0.6)
        fsc_window.attributes("-topmost",True)
        fsc_window.attributes("-fullscreen",True)

        cv=tk.Canvas(fsc_window,bg="white")
        cv.place(x=0,y=0,width=fsc_window.winfo_screenwidth(),height=fsc_window.winfo_screenheight())

        def grab(event):
            if not((self.end_x-self.start_x==0)and(self.end_y-self.start_y==0)):
                if not((self.end_x<self.start_x)or(self.end_y<self.start_y)):
                    self.image=self.image.crop((self.start_x,self.start_y,self.end_x,self.end_y))#再把全屏截图截取指定部分
                    fsc_window.destroy()
                    main_window.attributes("-alpha",1)   
                    save(main_window,self.image)

            self.start_x=self.start_y=self.end_x=self.end_y=0

        def start(event):
            self.start_x,self.start_y=event.x,event.y

        def OnDrag(event):
            self.end_x=event.x
            self.end_y=event.y
            cv.delete("all")
            cv.create_rectangle(self.start_x,self.start_y,self.end_x-self.start_x,self.end_y-self.start_y,fill="black")

        def close(event):
            fsc_window.destroy()

        fsc_window.bind("<ButtonRelease-1>",grab)
        fsc_window.bind("<Button-1>",start)
        fsc_window.bind("<B1-Motion>",OnDrag)
        fsc_window.bind("<Escape>",close)

    def GIF_begin(self):
        while True:
            self.frames.append(ImageGrab.grab((self.start_x,self.start_y,self.end_x,self.end_y)))
            time.sleep(1/24)

    def GIF_screenshot(self,main_window,mode=settings["gif-save-mode"]):
        #初始化
        fsc_window=tk.Toplevel(main_window)
        fsc_window.attributes("-alpha",0.6)
        fsc_window.attributes("-topmost",True)
        fsc_window.attributes("-fullscreen",True)

        cv=tk.Canvas(fsc_window,bg="white")
        cv.place(x=0,y=0,width=fsc_window.winfo_screenwidth(),height=fsc_window.winfo_screenheight())

        def start(event):
            #结束划定区域，开始录GIF
            is_doing=tk.BooleanVar(main_window,True)
            fsc_window.destroy()
            #创建并且初始化工具条窗口
            tool_bar=tk.Toplevel(main_window)
            tool_bar.geometry(f"100x25+{tool_bar.winfo_screenwidth()-100}+{int(tool_bar.winfo_screenheight()/2)}")
            tool_bar.attributes("-topmost",True)
            tool_bar.overrideredirect(True)

            def stop_GIF():
                threading.Thread._Thread__stop(self.GIF_thread)
                
                file_path=settings["image-save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".gif"
                self.frames[0].save(file_path,append_images=self.frames[1:],save_all=True,loop=True)
                success_msg(main_window,"gif",file_path)
            
            b1=tk.Button(tool_bar,text="stop",command=stop_GIF)
            b2=tk.Button(tool_bar,text="exit",command=lambda:tool_bar.destroy())
            b1.place(x=0,y=0,width=50,height=25)
            b2.place(x=50,y=0,width=50,height=25)
            #开始录屏GIF
            if not((self.end_x-self.start_x==0)and(self.end_y-self.start_y==0)):
                if self.end_x<self.start_x:
                    self.start_x,self.end_x=self.end_x,self.start_x
                elif self.end_y<self.start_y:
                    self.start_y,self.end_y=self.end_y,self.start_y

                self.GIF_thread.start()
                self.GIF_thread.join()

            self.start_x=self.start_y=self.end_x=self.end_y=0

        def press(event):
            #按下左键开始划定区域
            self.start_x,self.start_y=event.x,event.y

        def OnDrag(event):
            #正在拖拽
            self.end_x=event.x
            self.end_y=event.y
            cv.delete("all")
            cv.create_rectangle(self.start_x,self.start_y,self.end_x-self.start_x,self.end_y-self.start_y,fill="black")

        def close(event):
            #关闭全屏窗口
            fsc_window.destroy()

        fsc_window.bind("<ButtonRelease-1>",start)
        fsc_window.bind("<Button-1>",press)
        fsc_window.bind("<B1-Motion>",OnDrag)
        fsc_window.bind("<Escape>",close)

    def video_begin(self):
        pass

    def video_end(self):
        pass