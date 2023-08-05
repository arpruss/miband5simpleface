from PIL import Image,ImageDraw
from collections import namedtuple
import os

##
## Note: Run twice to get previews right
##


def resize(inFile,outFile,size):
    try:
        img = Image.open(inFile).convert('RGBA')
        img = img.resize(size,resample=Image.LANCZOS)
    except:
        print("Error resizing preview")
        img = Image.new('RGB', size)
    img.save(outFile,'PNG')

Digits = namedtuple("Digits", ("color", "size", "file", "index", "blankZero"), defaults=[None,None,None,None,False])
Battery = namedtuple("Battery", ("size", "backColor", "fullColor", "emptyColor", "index"))
DateSlash = namedtuple("Slash", ("size", "file", "color", "index"))

class Face(object):
    previewSize = (102,242)

    def __init__(self,name=None,json=None,timeDigit=None,hourTensDigit=None,battery=None,heartDigit=None,
            stepsDigit=None,dateDigit=None,dateSlash=None,jsonParams={},buildDirectory="build"):
        self.name = name
        self.json = json
        self.timeDigit = timeDigit
        self.hourTensDigit = hourTensDigit
        self.battery = battery
        self.heartDigit = heartDigit
        self.stepsDigit = stepsDigit
        self.dateDigit = dateDigit
        self.dateSlash = dateSlash
        self.jsonParams = jsonParams
        self.buildDirectory = buildDirectory
        
    def generateDigits(self,digits):
        print("Generating %04d" % self.index)
        self.jsonParams["index:" + digits.index] = self.index
        for i in range(10):
            self.generateCharacter(digits.file % i,digits.color,digits.size, blank=(digits.blankZero and i == 0))
            
    def generateBattery(self,b):
        print("Generating %04d" % self.index)
        self.jsonParams["index:" + b.index] = self.index
        for i in range(10):
            x = i / 9.
            img = Image.new('RGBA', b.size, b.backColor)
            draw = ImageDraw.Draw(img)
            w = int(x * b.size[0])
            c = []
            for j in range(4):
                c.append(int(b.fullColor[j]*x + b.emptyColor[j]*(1-x)))
            draw.rectangle([(b.size[0]//2-w//2,0),(b.size[0]//2+w//2),b.size[1]],fill=tuple(c))
            img.save("%s/%04d.png" % (self.buildDirectory, self.index), 'PNG')       
            self.index += 1

    def generateCharacter(self,inFile,color,size,blank=False):
        outFile = "%s/%04d.png" % (self.buildDirectory, self.index)
        print("From %s to %s" % (inFile, outFile))
        img = Image.open(inFile).convert('RGBA')
        img = img.resize(size,resample=Image.LANCZOS)
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                if blank:
                    out = (0,0,0,0)
                else:
                    pixel = img.getpixel((x,y))
                    out = tuple(color[i] if i < 3 else pixel[3] for i in range(4))
                img.putpixel((x,y),out)
        self.index += 1
        img.save(outFile, 'PNG')

    def generate(self):
        try:
            os.mkdir(self.buildDirectory)
        except:
            pass

        json = "%s/%s.json" % (self.buildDirectory, self.name)
        print(json)
        self.index = 0
            
        self.generateDigits(self.timeDigit)
        self.generateDigits(self.hourTensDigit)
        if self.heartDigit:
            self.generateDigits(self.heartDigit)
        if self.stepsDigit:
            self.generateDigits(self.stepsDigit)
        if self.dateDigit:
            self.generateDigits(self.dateDigit)
        if self.battery:
            self.generateBattery(self.battery)
        if self.dateSlash:
            self.jsonParams["index:" + self.dateSlash.index] = self.index
            self.generateCharacter(self.dateSlash.file,self.dateSlash.color,self.dateSlash.size)
        resize(json[:-5]+"_packed_preview.png", "%s/%04d.png" % (self.buildDirectory, self.index), Face.previewSize)
        self.jsonParams["index:preview"] = self.index
        self.index += 1
        
        print(self.jsonParams)
        
        with open(self.json) as f:
            with open(json, "w") as g:
                for line in f:
                    for x in self.jsonParams:
                        line = line.replace("$"+x+"$", str(self.jsonParams[x]))
                    g.write(line)

        os.system(os.path.join("..","WatchFace") + ' "' + json +'"')

