import time
import math
import threading
import numpy as np

TIME_DELAY_2_4 = 0xFF:0.0024  # 2.4ms - 1 cycle  - Max Count: 1024
R_DATAL = 0x16 # Red data line
G_DATAL = 0x18 #Green data line
B_DATAL = 0x1A # Blue data line
C_DATAL = 0x14 # Clear data line


cases = {0 : red,
         1 : orange,
         2 : yellow,
         3 : green,
         4 : blue,
         5 : inconclusive
        }

class ColorSensing:
    numFound = 0
    lookingFor = 0
    time.sleep(TIME_DELAY_2_4[self._integration_time])
    rarr = np.array(200)
    garr = np.array(200)
    barr = np.array(200)
    carr = np.array(200)
    while (isSolved() == false)
        for i in (0, 200)
            r, g, b, c = self.getValues()
            rarr = np.append(rarr, i, r)
            garr = np.append(garr, i, g)
            barr = np.append(barr, i, b)
            carr = np.append(carr, i, c)
        rMean = mean(rarr)
        gMean = mean (garr)
        bMean = mean(barr)
        cMean = mean(carr)
        r, g, b, c = scaleDown(rMean, gMean, bMean, cMean)



def getValues(self):
    r = self._device.readU8(R_DATAL)
    g = self._device.readU8(G_DATAL)
    b = self._device.readU8(B_DATAL)
    c = self._device.readU8(C_DATAL)
    self._integration_time = TIME_DELAY_2_4
    return (r, g, b, c)

def isSolved():
    if(numFound == 5)
        return True
    else
        return False

def mean(someArray):
    sum = 0
    count = 0
    for i in (0, len(someArray))
        if(someArray[i] < 5)
            continue
        elif(mean - math.abs(someArray[i] > 100)
            sum = sum + mean
            count = count + 1
        else
            sum = sum + someArray[i]
            count = count + 1
    mean = sum/count
    return mean


def scaleDown(r, g, b, c):
     r = r/c * 255.0
     g = g/c * 255.0
     b = b/c * 255.0
     c = c/255.0
     return (r, g, b, c)

#true or false depending on if match or not
def colorFound(r, g, b, c):
    if(r > b & r > g)
        if r > (b + g)
            found = 0
        elif (g >1.5*b)
            found = 2
        else 
            found = 1
    elif g > b
        found = 3
    elif b > g
        found = 4
    else 
        found = 5
    return found

def match(found){
    if (cases[found] == cases[lookingFor])
        return true
    else
        return false

}