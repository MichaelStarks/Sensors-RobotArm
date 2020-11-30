import time
import math
import numpy as np
import Adafruit_TCS34725

#R_DATAL = 0x16 # Red data line
#G_DATAL = 0x18 # Green data line
#B_DATAL = 0x1A # Blue data line
#C_DATAL = 0x14 # Clear data line
sensor = Adafruit_TCS34725.TCS34725()
sensor.set_interrupt(False)
found = 0
# lookingFor = 0

def mean(someArray):
    sum = 0
    count = 0
    mean = 0
    for i in range(0, len(someArray)):
        if(someArray[i] < 5):
            continue
        elif(mean - np.abs(someArray[i]) > 100):
            sum = sum + mean
            count = count + 1
            mean = sum/count
        else:
            sum = sum + someArray[i]
            count = count + 1
            mean = sum/count

        if (count==0):
            mean = 0
    return mean


def scaleDown(r, g, b, c):
    r = r/c * 255.0
    g = g/c * 255.0
    b = b/c * 255.0
    c = c/255.0
    return (r, g, b, c)

#true or false depending on if match or not
def colorFound(r, g, b, c):
    global found
    ratioR = r/c
    ratioG = g/c
    ratioB = b/c
    if(ratioR > ratioB) and (ratioR > ratioG):
        if (r > (b + g)):
            if (g > 1.25*b):
                found = 1
            else:
                found = 0
        else:
            found = 2
    elif (ratioG > ratioB) and (ratioG > ratioR):
        found = 3
    elif (ratioB > ratioG)and (ratioB > ratioR):
        found = 4
    else:
        found = 5
    return found

def match(found):
    if (cases[found] == cases[lookingFor]):
        return True
    else:
        return False

def isSolved():
        return False

cases = {0 : 'red',
    1 : 'orange',
    2 : 'yellow',
    3 : 'green',
    4 : 'blue',
    5 : 'inconclusive',
    }

def whoDis():
    rarr = np.empty(50)
    garr = np.empty(50)
    barr = np.empty(50)
    carr = np.empty(50)
    while (isSolved() == False):
        for i in range(0, 24):
            r, g, b, c = sensor.get_raw_data()
            rarr[i] = r
            garr[i] = g
            barr[i] = b
            carr[i] = c
            time.sleep(0.154)
            #print('Red:' + str(r), 'Green:' + str(g), 'Blue:' + str(b), 'Clear:' + str(c))
        rMean = mean(rarr)
        gMean = mean(garr)
        bMean = mean(barr)
        cMean = mean(carr)

        # print(rMean, gMean, bMean, cMean)
        #print('Red:' + str(rMean), 'Green:' + str(gMean), 'Blue:' + str(bMean), 'Clear:' + str(cMean))
        #r, g, b, c = scaleDown(rMean, gMean, bMean, cMean)
        # if (match(colorFound(r, g, b, c))):
        #      lookingFor = lookingFor + 1
        #      found = found + 1
        # print (r, g, b, c)
        print(cases[colorFound(r, g, b, c)])
        return cases[colorFound(r, g, b, c)]
