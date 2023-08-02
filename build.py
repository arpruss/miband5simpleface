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

bigDigit = Digits(color = (255,255,255,255), size = (60,86), file = "heavy%01d.png", index=0)
bigDigitHourTensBlankZero = Digits(color = (255,255,255,255), size = (60,86), file = "heavy%01d.png", index=10, blankZero = True)
bigDigitHourTensZeroZero = Digits(color = (255,255,255,255), size = (60,86), file = "heavy%01d.png", index=10, blankZero = False, )
heartDigit = Digits(color = (255,153,85,255), size = (34,46), file = "bold%01d.png", index=20)
stepsDigit = Digits(color = (255,255,0,255), size = (25,46), file = "bold%01d.png", index=30)
dateDigit = stepsDigit
battery = Battery(size=(128,2), backColor=(64,64,64,255), fullColor = (0,255,0,255), emptyColor = (255,0,0,255), index = 40)
dateSlash = None # DateSlash(file = "boldslash.png", size = dateDigit.size, color = dateDigit.color, index = 51)
previewSize = (104,328)
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

def generateCharacter(inFile,color,size,index,blank=False):
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
    outFile = "%s/%04d.png" % (buildDirectory, index)
    img.save(outFile, 'PNG')

def generateDigits(digits):
    print("Generating %04d" % digits.index)
    for i in range(10):
        generateCharacter(digits.file % i,digits.color,digits.size, digits.index, blank=(digits.blankZero and i == 0))
        
def generateBattery(b):
    print("Generating %04d" % b.index)
    for i in range(10):
        x = i / 9.
        img = Image.new('RGBA', b.size, b.backColor)
        draw = ImageDraw.Draw(img)
        w = int(x * b.size[0])
        c = []
        for j in range(4):
            c.append(int(b.fullColor[j]*x + b.emptyColor[j]*(1-x)))
        draw.rectangle([(b.size[0]//2-w//2,0),(b.size[0]//2+w//2),b.size[1]],fill=tuple(c))
        img.save("%s/%04d.png" % (buildDirectory, i+b.index), 'PNG')
    
try:
    os.mkdir(buildDirectory)
except:
    pass

for zero in (False,True):    
    json = "%s/%s-%s.json" % (buildDirectory, name, "leading-zero" if zero else "no-leading-zero")
    print(json)
    with open("miband5.json") as f:
        with open(json, "w") as g:
            g.write(f.read())

        
    generateDigits(bigDigit)
    if zero:
        generateDigits(bigDigitHourTensZeroZero)
    else:
        generateDigits(bigDigitHourTensBlankZero)
    generateDigits(heartDigit)
    generateDigits(stepsDigit)
    generateBattery(battery)
    if dateSlash:
        generateCharacter(dateSlash.file,dateSlash.color,dateSlash.size,dateSlash.index)
    
    resize(json[:-5]+"_packed_preview.png", "%s/%04d.png" % (buildDirectory, previewIndex), previewSize)
    
    os.system(os.path.join("..","WatchFace") + ' "' + json +'"')
