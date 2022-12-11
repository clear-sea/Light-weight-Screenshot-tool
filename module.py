from PIL import Image,ImageGrab
import json,os,datetime,wx,time

with open("settings.json","r",encoding="utf-8") as f:
    settings=json.load(f)
    
def create_dirs(path):
    if not os.path.exists(path):
        os.mkdir(path)
alpha=200
def success_msgbox(image,mode):
    '''
        image:PIL Image type;
        mode:"image","gif","video"
    '''
    global alpha

    screen_size=wx.DisplaySize()
    msg=wx.Frame(None,size=(200,100),pos=(screen_size[0]-200,screen_size[1]-100),style=wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
    msg.Show()

    text=wx.StaticText(msg,label="截图成功")
    text.Show()

    picture=wx.Image(image,wx.BITMAP_TYPE_ANY)
    picture.Scale(100,100)
    picture=wx.StaticBitmap(msg,-1,wx.BitmapFromImage(picture))
    picture.Show()

    time.sleep(2)
    msg.Destroy()

class ImageShot:
    def __init__(self):
        pass
    def full_screenshot(self,mode=settings["image-save-mode"]):
        image=ImageGrab.grab()
        if mode=="file-save":
            create_dirs(settings["image-save-path"])
            image.save(settings["image-save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".jpg")

            success_msgbox(settings["image-save-path"]+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".jpg","image")

    def rect_screenshot(self,path,mode=settings["image-save-mode"]):
        pass