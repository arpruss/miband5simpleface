from PIL import Image,ImageDraw

height = 2
width = 128
backColor = (64,64,64,255)
fullColor = (0,255,0,255)
emptyColor = (255,0,0,255)


for i in range(10):
    x = i / 9.
    img = Image.new('RGBA', (width,height), backColor)
    draw = ImageDraw.Draw(img)
    w = int(x * width)
    c = []
    for j in range(4):
        c.append(int(fullColor[j]*x + emptyColor[j]*(1-x)))
    draw.rectangle([(width//2-w//2,0),(width//2+w//2),height],fill=tuple(c))
    img.save("battery%02d.png" % i, 'PNG')
    
    
    