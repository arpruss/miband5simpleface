from PIL import Image,ImageDraw
from collections import namedtuple
import os

##
## Note: Run twice to get previews right
##

name = "BigAndSimple"

Digits = namedtuple("Digits", ("color", "size", "file", "index", "blankZero"), defaults=[None,None,None,None,False])

batteryHeight = 2
batteryWidth = 128
batteryBackColor = (64,64,64,255)
batteryFullColor = (0,255,0,255)
batteryEmptyColor = (255,0,0,255)

bigDigit = Digits(color = (255,255,255,255), size = (60,86), file = "heavy%01d.png", index=0)
bigDigitHourTensBlankZero = Digits(color = (255,255,255,255), size = (60,86), file = "heavy%01d.png", index=10, blankZero = True)
bigDigitHourTensZeroZero = Digits(color = (255,255,255,255), size = (60,86), file = "heavy%01d.png", index=10, blankZero = False, )
heartDigit = Digits(color = (255,153,85,255), size = (34,46), file = "bold%01d.png", index=20)
stepsDigit = Digits(color = (255,255,0,255), size = (25,46), file = "bold%01d.png", index=30)
previewSize = (104,328)
batteryIndex = 40
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

def generateDigit(inFile,color,size,outFile,blank=False):
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
    img.save(outFile, 'PNG')

def generateDigits(digits):
    print("Generating %04d" % digits.index)
    for i in range(10):
        generateDigit(digits.file % i,digits.color,digits.size, "%s/%04d.png" % (buildDirectory, digits.index+i),blank=(digits.blankZero and i == 0))
    
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

    # generate battery
    print("Generating %04d" % batteryIndex)
    for i in range(10):
        x = i / 9.
        img = Image.new('RGBA', (batteryWidth,batteryHeight), batteryBackColor)
        draw = ImageDraw.Draw(img)
        w = int(x * batteryWidth)
        c = []
        for j in range(4):
            c.append(int(batteryFullColor[j]*x + batteryEmptyColor[j]*(1-x)))
        draw.rectangle([(batteryWidth//2-w//2,0),(batteryWidth//2+w//2),batteryHeight],fill=tuple(c))
        img.save("%s/%04d.png" % (buildDirectory, i+batteryIndex), 'PNG')
        
    generateDigits(bigDigit)
    if zero:
        generateDigits(bigDigitHourTensZeroZero)
    else:
        generateDigits(bigDigitHourTensBlankZero)
    generateDigits(heartDigit)
    generateDigits(stepsDigit)
    
    resize(json[:-5]+"_packed_preview.png", "%s/%04d.png" % (buildDirectory, previewIndex), previewSize)
    
    os.system(os.path.join("..","WatchFace") + ' "' + json +'"')
