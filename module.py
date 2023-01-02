from PIL import Image,ImageGrab
import json,os,datetime,wx,threading

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
    msg=wx.Frame(None,size=(200,100),pos=(screen_size[0]-200,screen_size[1]-100),style=wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
    msg.Show()
    msg.SetTransparent(150)

    def close(event):
        msg.SetSize(180,80)
        msg.Close()
    def open_image(event):
        os.system(f"explorer {file_path}")

    msg.Bind(wx.EVT_LEFT_DOWN,close)

    t0=wx.StaticText(msg,label="截图成功(左键单击关闭)",pos=(0,0))
    t1=wx.StaticText(msg,label=f"已保存在{file_path},点击打开",pos=(0,50))
    t1.Bind(wx.EVT_LEFT_DOWN,open_image)
    t1.Show()
    t0.Show()


class ImageShot:
    def __init__(self):
        pass
    def full_screenshot(self,mode=settings["image-save-mode"]):
        image=ImageGrab.grab()
        if mode=="file-save":
            create_dirs(settings["image-save-path"])
            file_path=settings["image-save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".jpg"
            image.save(file_path)
            
            success_msg(image,"image",file_path)

    def rect_screenshot(self,path,mode=settings["image-save-mode"]):
        pass