import wx,threading,grab,pynput

app=wx.App()
#创建主窗口
#主窗口初始化
main_window=grab.Window(None,size=(400,100),style=wx.SIMPLE_BORDER)
main_window.Center()
main_window.Show()
#创建截图功能类
screenshot=grab.ScreenShot()
#功能
def full_screenshot(event):
    image=screenshot.full_screenshot(main_window)
    grab.save(image)

def rect_screenshot(event):
    image=screenshot.rect_screenshot(main_window)
    grab.save(image)

#按钮
#0
font=wx.Font(15,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
btn1=wx.Button(main_window.p2,label="全屏截图",pos=(0,0),size=(100,100))
btn1.SetFont(font)
btn1.Show()
btn1.SetCursor(wx.Cursor(wx.CURSOR_HAND))

btn1.Bind(wx.EVT_BUTTON,full_screenshot)
#1
btn2=wx.Button(main_window.p2,label="",pos=(100,0),size=(100,100))
btn2.SetFont(font)
btn2.Show()
btn2.SetCursor(wx.Cursor(wx.CURSOR_HAND))
btn2.Bind(wx.EVT_BUTTON,rect_screenshot)


app.MainLoop()