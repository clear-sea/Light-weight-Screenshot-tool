from PIL import Image,ImageGrab
import json,os,datetime,wx

#主窗口类
class Window(wx.Frame):
    def __init__(self,*args,**kw):
        super().__init__(*args,**kw)
        #初始化
        self.p1=wx.Panel(self,pos=(0,0),size=(400,30))
        self.p1.Show()
        self.p2=wx.Panel(self,pos=(0,30),size=(400,100))
        self.p2.Show()
        self.p2.SetBackgroundColour(wx.WHITE)

        self.width,self.height=400,130

        self.SetSize(self.width,self.height)

        self.title=wx.StaticText(self.p1,label="LightScreenShot",pos=(30,0),size=(self.width-60,30))
        self.title.Show()
        self.title.SetFont(wx.Font(20,wx.DEFAULT,wx.NORMAL,wx.NORMAL))
        self.title.SetBackgroundColour(wx.WHITE)

        self.icon=wx.StaticBitmap(self.p1,bitmap=wx.Image("images/icon.jpg").ConvertToBitmap(),pos=(0,0))
        self.icon.Show()

        self.close_btn=wx.StaticBitmap(self.p1,bitmap=wx.Image("images/close0.png").ConvertToBitmap(),pos=(self.width-30,0))
        self.close_btn.Show()
        #绑定事件
        self.close_btn.Bind(wx.EVT_LEFT_DOWN,self.Windowsclose)

        for widget in [self,self.p1,self.p2,self.icon,self.title]:
            widget.Bind(wx.EVT_LEFT_DOWN, self.OnPanelLeftDown)
            widget.Bind(wx.EVT_MOTION, self.OnPanelMotion)
            widget.Bind(wx.EVT_LEFT_UP, self.OnPanelLeftUp)
        
    def OnPanelLeftDown(self, event):
        pos = event.GetPosition()
        x, y = self.ClientToScreen(event.GetPosition())
        ox, oy = self.GetPosition()
        dx = x - ox
        dy = y - oy
        self.delta = ((dx, dy))
 
    def OnPanelMotion(self, event):
        if event.Dragging() and event.LeftIsDown():
            mouse=wx.GetMousePosition()
            self.Move((mouse.x-self.delta[0],mouse.y-self.delta[1]))
 
    def OnPanelLeftUp(self, event):
        if self.HasCapture():
            self.ReleaseMouse()

    def Windowsclose(self,event):
        self.Close()#⚠️后期改为隐藏窗口


with open("settings.json","r",encoding="utf-8") as f:
    settings=json.load(f)
    
def create_dirs(path):
    if not os.path.exists(path):
        os.mkdir(path)

def success_msg(image,mode,file_path):
    '''
        image:PIL Image type;
        mode:"image","gif","video"
    '''
    screen_size=wx.DisplaySize()
    msg=wx.Frame(None,size=(230,100),pos=(screen_size[0]-200,screen_size[1]-100),style=wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
    msg.Show()
    msg.SetTransparent(150)

    def close(event):
        msg.Close()
    def open_image(event):
        Image.open(file_path).show()


    msg.Bind(wx.EVT_LEFT_DOWN,close)

    if mode=="image":
        info="截图成功(左键单击关闭)"
    elif mode=="gif":
        info="录制GIF结束(左键单击关闭)"
    elif mode=="video":
        info="录制视频结束(左键单击关闭)"
    else:
        info=None

    t0=wx.StaticText(msg,label=info,pos=(0,0))
    t1=wx.StaticText(msg,label=f"已保存在:\n{file_path}\n点击打开",pos=(0,20))
    t1.SetFont(wx.Font(8,wx.DEFAULT,wx.NORMAL,wx.NORMAL,underline=True))
    t1.Bind(wx.EVT_LEFT_DOWN,open_image)
    t1.Show()
    t0.Show()

def save(image,mode=settings["image-save-mode"]):
    if mode=="file-save":
        create_dirs(settings["image-save-path"])
        file_path=settings["image-save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".jpg"
        image.save(file_path)
        
        success_msg(image,"image",file_path)

class ScreenShot:
    def full_screenshot(self,main_window):
        main_window.Show(False)
        self.image=ImageGrab.grab()
        main_window.Show(True)
        return self.image

    def rect_screenshot(self,main_window):
        main_window.Show(False)
        #初始化
        fsc_window=wx.Frame(main_window,style=wx.STAY_ON_TOP)
        fsc_window.ShowFullScreen(True)
        fsc_window.SetTransparent(100)
        dc=wx.ClientDC(fsc_window)

        self.start_x=0
        self.start_y=0
        self.end_x=0
        self.end_y=0

        def grab(event):
            main_window.Show(False)
            self.image=ImageGrab.grab()
            main_window.Show(True)
            fsc_window.Close()

        def start(event):
            pos=event.GetPosition()
            self.start_x,self.start_y=pos.x,pos.y

        def OnDrag(event):
            dc.Clear()
            pos=event.GetPosition()
            dc.DrawRectangle(self.start_x,self.start_y,self.end_x-self.start_x,self.end_y-self.start_y)

        def close(event):
            if event.GetKeyCode()==wx.WXK_ESCAPE:
                fsc_window.Close()

        fsc_window.Bind(wx.EVT_RIGHT_DOWN,grab)
        fsc_window.Bind(wx.EVT_LEFT_DOWN,start)
        fsc_window.Bind(wx.EVT_MOTION,OnDrag)
        fsc_window.Bind(wx.EVT_KEY_DOWN,close)

        main_window.Show(True)

        return self.image

    def GIF_begin(self,path,mode=settings["gif-save-mode"]):
        image=ImageGrab.grab()
        

    def GIF_end(self):
        pass

    def video_begin(self):
        pass

    def video_end(self):
        pass