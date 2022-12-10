import wx,threading

app=wx.App()

main_window=wx.Frame(None,title="LightScreenShot")
main_window.Show()

main_window.SetIcon(wx.Icon('images/icon.jpg'))
main_window.SetSize((800,600))
main_window.Center()

btn=wx.Button(main_window,label="Full",pos=(0,0))
btn.Show()
btn.Bind()

app.MainLoop()