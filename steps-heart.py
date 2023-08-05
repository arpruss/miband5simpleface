from MiBand5Face import *

##
## Note: Run twice to get previews right
##



bigDigit = Digits(color = (255,255,255,255), size = (60,86), file = "heavy%01d.png", index="bigDigits")
bigDigitHourTensBlankZero = Digits(color = (255,255,255,255), size = bigDigit.size, file = "heavy%01d.png", index="tensDigits", blankZero = True)
bigDigitHourTensZeroZero = Digits(color = (255,255,255,255), size = bigDigit.size, file = "heavy%01d.png", index="tensDigits", blankZero = False)
heartDigit = Digits(color = (255,153,85,255), size = (34,46), file = "bold%01d.png", index="heartDigits")
stepsDigit = Digits(color = (255,255,0,255), size = (25,46), file = "bold%01d.png", index="stepsDigits")
dateDigit = Digits(color = (255,255,0,255), size = (25,46), file = "bold%01d.png", index="dateDigits")
battery = Battery(size=(128,3), backColor=(32,32,32,255), fullColor = (0,255,0,255), emptyColor = (128,128,0,255), index="battery")
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



        
    

heartStepsNoZero.generate()
heartStepsZero.generate()
lightHeartStepsNoZero.generate()
lightHeartStepsZero.generate()