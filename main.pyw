import threading,grab,pynput
import tkinter as tk

#创建主窗口
#主窗口初始化
main_window=tk.Tk()
main_window.geometry("400x100")
main_window.iconbitmap("images/icon.ico")
main_window.resizable(False,False)
main_window.title("LightScreenShot")
main_window["bg"]="white"
#创建截图功能类
screenshot=grab.ScreenShot()
#功能
def full_screenshot():
    screenshot.full_screenshot(main_window)

def rect_screenshot():
    screenshot.rect_screenshot(main_window)

def GIF_screenshot():
    screenshot.GIF_screenshot(main_window)

#全屏
btn1=tk.Button(main_window,bg="white",text="全屏截图",cursor="hand2",command=full_screenshot)
btn1.place(x=0,y=0,width=100,height=100)
#矩形
btn2=tk.Button(main_window,bg="white",text="矩形截图",cursor="hand2",command=rect_screenshot)
btn2.place(x=100,y=0,width=100,height=100)
#GIF
btn3=tk.Button(main_window,bg="white",text="GIF截图",cursor="hand2",command=GIF_screenshot)
btn3.place(x=200,y=0,width=100,height=100)

main_window.mainloop()