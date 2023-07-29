from PIL import Image,ImageDraw
import os

batteryHeight = 2
batteryWidth = 128
batteryBackColor = (64,64,64,255)
batteryFullColor = (0,255,0,255)
batteryEmptyColor = (255,0,0,255)
bigDigitColor = (255,255,255,255)
bigDigitSize = (60,85)
bigDigitFile = "heavy%01d.png"
zeroTensHourDigit = False
heartDigitColor = (255,153,85,255)
heartDigitSize = (30,42)
heartDigitFile = "bold%01d.png"
stepsDigitColor = (255,255,0,255)
stepsDigitSize = (24,42)
stepsDigitFile = "bold%01d.png"

bigDigitNormalIndex = 0
bigDigitHourTensIndex = 10
batteryIndex = 20
heartDigitIndex = 30
stepsDigitIndex = 40
buildDirectory = "build"

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
    
        

def generateDigits(inName,color,size,index,blankZero=False):
    print("Generating %04d" % index)
    for i in range(10):
        generateDigit(inName % i,color,size, "%s/%04d.png" % (buildDirectory, index+i),blank=(blankZero and i == 0))
    

try:
    os.mkdir(buildDirectory)
except:
    pass
    
with open("miband5.json") as f:
    with open("%s/miband5.json" % buildDirectory, "w") as g:
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
    
generateDigits(bigDigitFile,bigDigitColor,bigDigitSize,bigDigitNormalIndex)
generateDigits(bigDigitFile,bigDigitColor,bigDigitSize,bigDigitHourTensIndex,blankZero=False if zeroTensHourDigit else True)
generateDigits(heartDigitFile,heartDigitColor,heartDigitSize,heartDigitIndex)
generateDigits(stepsDigitFile,stepsDigitColor,stepsDigitSize,stepsDigitIndex)
os.system(os.path.join("..","Mi.Band.WatchFace.Editor","WatchFace","WatchFace") + " build/miband5.json")
