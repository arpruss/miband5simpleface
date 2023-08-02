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
Face = namedtuple("Face", ("name","json","timeDigit", "hourTensDigit", "battery", "heartDigit", 
            "stepsDigit", "dateDigit", "dateSlash"), defaults=(None,)*9)

bigDigit = Digits(color = (255,255,255,255), size = (60,86), file = "heavy%01d.png", index=0)
bigDigitHourTensBlankZero = Digits(color = (255,255,255,255), size = (60,86), file = "heavy%01d.png", index=10, blankZero = True)
bigDigitHourTensZeroZero = Digits(color = (255,255,255,255), size = (60,86), file = "heavy%01d.png", index=10, blankZero = False)
heartDigit = Digits(color = (255,153,85,255), size = (34,46), file = "bold%01d.png", index=20)
stepsDigit = Digits(color = (255,255,0,255), size = (25,46), file = "bold%01d.png", index=30)
dateDigit = stepsDigit
battery = Battery(size=(128,2), backColor=(64,64,64,255), fullColor = (0,255,0,255), emptyColor = (255,0,0,255), index = 40)
dateSlash = DateSlash(file = "boldslash.png", size = dateDigit.size, color = dateDigit.color, index = 51)

lightBigDigit = Digits(color = (0,0,0,255), size = (60,86), file = "heavy%01d.png", index=0)
lightBigDigitHourTensBlankZero = Digits(color = (0,0,0,255), size = (60,86), file = "heavy%01d.png", index=10, blankZero = True)
lightBigDigitHourTensZeroZero = Digits(color = (0,0,0,255), size = (60,86), file = "heavy%01d.png", index=10, blankZero = False)
lightHeartDigit = Digits(color = (128,0,0,255), size = (34,46), file = "bold%01d.png", index=20)
lightStepsDigit = Digits(color = (0,64,0,255), size = (25,46), file = "bold%01d.png", index=30)
lightDateDigit = lightStepsDigit
lightBattery = Battery(size=(128,2), backColor=(128,128,128,255), fullColor = (0,128,0,255), emptyColor = (128,0,0,255), index = 40)
lightDateSlash = DateSlash(file = "boldslash.png", size = lightDateDigit.size, color = lightDateDigit.color, index = 51)



heartStepsNoZero = Face(name="heart-steps-no-zero", json="miband5.json", timeDigit=bigDigit, hourTensDigit=bigDigitHourTensBlankZero,
                        battery=battery, heartDigit=heartDigit, stepsDigit=stepsDigit)
heartStepsZero = Face(name="heart-steps-zero", json="miband5.json", timeDigit=bigDigit, hourTensDigit=bigDigitHourTensZeroZero,
                        battery=battery, heartDigit=heartDigit, stepsDigit=stepsDigit)
lightHeartStepsNoZero = Face(name="light-heart-steps-no-zero", json="light.json", timeDigit=lightBigDigit, 
                        hourTensDigit=lightBigDigitHourTensBlankZero,
                        battery=lightBattery, heartDigit=lightHeartDigit, stepsDigit=lightStepsDigit)
lightHeartStepsZero = Face(name="light-heart-steps-zero", json="light.json", timeDigit=lightBigDigit, hourTensDigit=lightBigDigitHourTensZeroZero,
                        battery=lightBattery, heartDigit=lightHeartDigit, stepsDigit=lightStepsDigit)

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
    print("From %s to %d" % (inFile, index))
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
        generateCharacter(digits.file % i,digits.color,digits.size, digits.index+i, blank=(digits.blankZero and i == 0))
        
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
        
def generateFace(face):
    json = "%s/%s.json" % (buildDirectory, face.name)
    print(json)
    with open(face.json) as f:
        with open(json, "w") as g:
            g.write(f.read())

        
    generateDigits(face.timeDigit)
    generateDigits(face.hourTensDigit)
    if face.heartDigit:
        generateDigits(face.heartDigit)
    if face.stepsDigit:
        generateDigits(face.stepsDigit)
    if face.battery:
        generateBattery(face.battery)
    if face.dateSlash:
        generateCharacter(face.dateSlash.file,face.dateSlash.color,face.dateSlash.size,face.dateSlash.index)
    
    resize(json[:-5]+"_packed_preview.png", "%s/%04d.png" % (buildDirectory, previewIndex), previewSize)
    
    os.system(os.path.join("..","WatchFace") + ' "' + json +'"')
    
try:
    os.mkdir(buildDirectory)
except:
    pass

generateFace(heartStepsNoZero)
generateFace(heartStepsZero)
generateFace(lightHeartStepsNoZero)
generateFace(lightHeartStepsZero)