import wx,threading,module,pynput

app=wx.App()
#创建主窗口
main_window=wx.Frame(None,title="LightScreenShot")
main_window.Show()
#设置主窗口
main_window.SetIcon(wx.Icon('images/icon.jpg'))
main_window.SetSize((800,600))
main_window.Center()
#实例化类
ImageShot=module.ImageShot()
#功能
def full_screenshot(event):
    ImageShot.full_screenshot()
#按钮
btn=wx.Button(main_window,label="✅",pos=(0,0))
btn.Show()

btn.Bind(wx.EVT_BUTTON,full_screenshot)

app.MainLoop()