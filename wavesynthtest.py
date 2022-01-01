import math

def waveSynth(freq,power,duration=1,waveform="sine",lowcut=0,highcut=100, stepSize=0.01):
    if (len(power) != 3 or len(freq) != 3):
        return -1 #arrays are not the right size
    else:
        motors=[]
        #we use 628 points per second, so the duration value can scale this
        totalPoints=(duration*6.28)/stepSize
        timing=[]
        for motor in range(0,1):
            print("***")
            #generate a sine wave
            temp=[]
            #generate one cycle of a sine wave
            x=0
           
            while (round(x,2) < (duration*6.28)):
                tempVal=((math.sin((x*freq[motor]))+1)*power[motor]/2) #scale in the x domain (to control frequency) and in the y domain to control how the power is mpped to motor power
                if waveform == "square": #if user asked for a square wave then threshold the sine wave
                    if (tempval > 50):
                        tempVal=100
                    else:
                        tempVal=0
                if tempVal < lowcut:
                    tempVal=lowcut
                if tempVal > highcut:
                    tempVal=highcut
                temp.append(tempVal)
                x=x+stepSize
            motors.append(temp)
        for i in range(0,round(totalPoints)): #generate the timing array
            timing.append(1/totalPoints)
        return [motors,timing]

print(str(waveSynth([20,20,20],[100,100,00],duration=0.1)))
