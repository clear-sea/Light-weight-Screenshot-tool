from PIL import Image,ImageGrab
import json

with open("settings.json","r",encoding="utf-8") as f:
    settings=json.load(f)

class ImageShot:
    def full_screenshot(self,path,mode=settings["image-save-mode"]):
        image=ImageGrab.grab()
        if mode=="file-save":
            image.save(settings["save-path"]+"//images")
      
