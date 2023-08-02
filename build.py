from PIL import Image,ImageDraw
from collections import namedtuple
import os

##
## Note: Run twice to get previews right
##

name = "BigAndSimple"

Digits = namedtuple("Digits", ("color", "size", "file", "index", "blankZero"), defaults=[None,None,None,None,False])
Battery = namedtuple("Battery", ("size", "backColor", "fullColor", "emptyColor", "index"))
DateSlash = namedtuple("Slash", ("size", "file", "color", "index"))

class Face(object):
    def __init__(self,name=None,json=None,timeDigit=None,hourTensDigit=None,battery=None,heartDigit=None,
            stepsDigit=None,dateDigit=None,dateSlash=None,jsonParams={}):
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
            img.save("%s/%04d.png" % (buildDirectory, self.index), 'PNG')       
            self.index += 1

    def generateCharacter(self,inFile,color,size,blank=False):
        outFile = "%s/%04d.png" % (buildDirectory, self.index)
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
        json = "%s/%s.json" % (buildDirectory, self.name)
        print(json)
        self.index = 0
            
        self.generateDigits(self.timeDigit)
        self.generateDigits(self.hourTensDigit)
        if self.heartDigit:
            self.generateDigits(self.heartDigit)
        if self.stepsDigit:
            self.generateDigits(self.stepsDigit)
        if self.battery:
            self.generateBattery(self.battery)
        if self.dateSlash:
            self.generateCharacter(self.dateSlash.file,self.dateSlash.color,self.dateSlash.size)
        resize(json[:-5]+"_packed_preview.png", "%s/%04d.png" % (buildDirectory, self.index), previewSize)
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


bigDigit = Digits(color = (255,255,255,255), size = (60,86), file = "heavy%01d.png", index="bigDigits")
bigDigitHourTensBlankZero = Digits(color = (255,255,255,255), size = bigDigit.size, file = "heavy%01d.png", index="tensDigits", blankZero = True)
bigDigitHourTensZeroZero = Digits(color = (255,255,255,255), size = bigDigit.size, file = "heavy%01d.png", index="tensDigits", blankZero = False)
heartDigit = Digits(color = (255,153,85,255), size = (34,46), file = "bold%01d.png", index="heartDigits")
stepsDigit = Digits(color = (255,255,0,255), size = (25,46), file = "bold%01d.png", index="stepsDigits")
dateDigit = Digits(color = (255,255,0,255), size = (25,46), file = "bold%01d.png", index="dateDigits")
battery = Battery(size=(128,3), backColor=(64,64,64,255), fullColor = (0,255,0,255), emptyColor = (255,0,0,255), index="battery")
dateSlash = DateSlash(file = "boldslash.png", size = dateDigit.size, color = dateDigit.color, index = "slash")

lightBigDigit = Digits(color = (0,0,0,255), size = bigDigit.size, file = "bold%01d.png", index="bigDigits")
lightBigDigitHourTensBlankZero = Digits(color = (0,0,0,255), size = lightBigDigit.size, file = "bold%01d.png", index="tensDigits", blankZero = True)
lightBigDigitHourTensZeroZero = Digits(color = (0,0,0,255), size = lightBigDigit.size, file = "bold%01d.png", index="tensDigits", blankZero = False)
lightHeartDigit = Digits(color = (128,0,0,255), size = heartDigit.size, file = "bold%01d.png", index="heartDigits")
lightStepsDigit = Digits(color = (0,64,0,255), size = stepsDigit.size, file = "bold%01d.png", index="stepsDigits")
lightDateDigit = Digits(color = (0,64,0,255), size = stepsDigit.size, file = "bold%01d.png", index="dateDigits")
lightBattery = Battery(size=battery.size, backColor=(160,160,160,255), fullColor = (0,128,0,255), emptyColor = (128,0,0,255), index = "battery")
lightDateSlash = DateSlash(file = "boldslash.png", size = lightDateDigit.size, color = lightDateDigit.color, index = "slash")

heartStepsNoZero = Face(name="heart-steps-no-zero", json="miband5.json", timeDigit=bigDigit, hourTensDigit=bigDigitHourTensBlankZero,
                        battery=battery, heartDigit=heartDigit, stepsDigit=stepsDigit, jsonParams={"background":'"0x000000"'})
heartStepsZero = Face(name="heart-steps-zero", json="miband5.json", timeDigit=bigDigit, hourTensDigit=bigDigitHourTensZeroZero,
                        battery=battery, heartDigit=heartDigit, stepsDigit=stepsDigit, jsonParams={"background":'"0x000000"'})
lightHeartStepsNoZero = Face(name="light-heart-steps-no-zero", json="light.json", timeDigit=lightBigDigit, 
                        hourTensDigit=lightBigDigitHourTensBlankZero,
                        battery=lightBattery, heartDigit=lightHeartDigit, stepsDigit=lightStepsDigit, jsonParams={"background":'"0xFFFFFF"'})
lightHeartStepsZero = Face(name="light-heart-steps-zero", json="light.json", timeDigit=lightBigDigit, hourTensDigit=lightBigDigitHourTensZeroZero,
                        battery=lightBattery, heartDigit=lightHeartDigit, stepsDigit=lightStepsDigit, jsonParams={"background":'"0xFFFFFF"'})

previewSize = (102,242)
previewIndex = 50
buildDirectory = "build"

def resize(inFile,outFile,size):
    try:
        img = Image.open(inFile).convert('RGBA')
        img = img.resize(size,resample=Image.LANCZOS)
    except:
        print("Error resizing preview")
        img = Image.new('RGB', size)
    img.save(outFile,'PNG')


        
    
try:
    os.mkdir(buildDirectory)
except:
    pass

heartStepsNoZero.generate()
heartStepsZero.generate()
lightHeartStepsNoZero.generate()
lightHeartStepsZero.generate()