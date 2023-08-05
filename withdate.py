from MiBand5Face import *

##
## Note: Run twice to get previews right
##



bigDigit = Digits(color = (255,255,255,255), size = (60,74), file = "heavy%01d.png", index="bigDigits")
bigDigitHourTensBlankZero = Digits(color = (255,255,255,255), size = bigDigit.size, file = "heavy%01d.png", index="tensDigits", blankZero = True)
bigDigitHourTensZeroZero = Digits(color = (255,255,255,255), size = bigDigit.size, file = "heavy%01d.png", index="tensDigits", blankZero = False)
heartDigit = Digits(color = (255,153,85,255), size = (34,44), file = "bold%01d.png", index="heartDigits")
stepsDigit = Digits(color = (255,255,0,255), size = (25,44), file = "bold%01d.png", index="stepsDigits")
dateDigit = Digits(color = (0,255,255,255), size = (25,44), file = "bold%01d.png", index="dateDigits")
battery = Battery(size=(128,3), backColor=(32,32,32,255), fullColor = (0,255,0,255), emptyColor = (128,128,0,255), index="battery")
dateSlash = DateSlash(file = "boldslash.png", size = dateDigit.size, color = dateDigit.color, index = "slash")

dateHeartStepsNoZero = Face(name="date-heart-steps-no-zero", json="withdate.json", timeDigit=bigDigit, hourTensDigit=bigDigitHourTensBlankZero,
                        battery=battery, heartDigit=heartDigit, stepsDigit=stepsDigit, dateDigit=dateDigit, dateSlash=dateSlash,
                        jsonParams={"background":'"0x000000"'})
dateHeartStepsZero = Face(name="date-heart-steps-zero", json="withdate.json", timeDigit=bigDigit, hourTensDigit=bigDigitHourTensZeroZero,
                        battery=battery, heartDigit=heartDigit, stepsDigit=stepsDigit, dateDigit=dateDigit, dateSlash=dateSlash,
                        jsonParams={"background":'"0x000000"'})



        
    

dateHeartStepsNoZero.generate()
dateHeartStepsZero.generate()
