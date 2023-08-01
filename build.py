from PIL import Image,ImageDraw
import os

##
## Note: Run twice to get previews right
##

name = "BigAndSimple"
batteryHeight = 2
batteryWidth = 128
batteryBackColor = (64,64,64,255)
batteryFullColor = (0,255,0,255)
batteryEmptyColor = (255,0,0,255)
bigDigitColor = (255,255,255,255)
bigDigitSize = (60,86)
bigDigitFile = "heavy%01d.png"
heartDigitColor = (255,153,85,255)
heartDigitSize = (34,46)
heartDigitFile = "bold%01d.png"
stepsDigitColor = (255,255,0,255)
stepsDigitSize = (25,46)
stepsDigitFile = "bold%01d.png"
previewSize = (104,328)

bigDigitNormalIndex = 0
bigDigitHourTensIndex = 10
batteryIndex = 20
heartDigitIndex = 30
stepsDigitIndex = 40
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

def generateDigits(inName,color,size,index,blankZero=False):
    print("Generating %04d" % index)
    for i in range(10):
        generateDigit(inName % i,color,size, "%s/%04d.png" % (buildDirectory, index+i),blank=(blankZero and i == 0))
    

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
        
    generateDigits(bigDigitFile,bigDigitColor,bigDigitSize,bigDigitNormalIndex)
    generateDigits(bigDigitFile,bigDigitColor,bigDigitSize,bigDigitHourTensIndex,blankZero=not zero)
    generateDigits(heartDigitFile,heartDigitColor,heartDigitSize,heartDigitIndex)
    generateDigits(stepsDigitFile,stepsDigitColor,stepsDigitSize,stepsDigitIndex)
    
    resize(json[:-5]+"_packed_preview.png", "%s/%04d.png" % (buildDirectory, previewIndex), previewSize)
    
    os.system(os.path.join("..","WatchFace") + ' "' + json +'"')
