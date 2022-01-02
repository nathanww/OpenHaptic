import math

def waveSynth(freq,power,duration=1,waveform="sine",lowcut=0,highcut=100, stepSize=0.01):
    if (len(power) != 3 or len(freq) != 3):
        return -1 #arrays are not the right size
    else:
        motors=[]
        #we use 628 points per second, so the duration value can scale this
        totalPoints=(duration*6.28)/stepSize
        timing=[]
        for motor in range(0,3):
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

def combineWaves(wave1,wave2,weight=1.0):
    newWave=[]
    """combines two waveforms (with equal duration) toghether.
    
    Arguments:
    wave1 -- list containing points in the first waveform
    wave2 -- list contianing points in the second waveform
    weight -- how much to weight the second waveform relative to the first. 1.0 is equal weight
    """
    if len(wave1) != len(wave2):
        print("Error, the two waves are not equal length")
        return -1
    else:
        for i in range(0,len(wave1)):
            #We combine add the two waves but scale the second by weight. Then we scale them so that the overall sum is the same as the original waveform
            temp=((wave1[i]/2)+((wave2[i]/2)*weight))
            #find the amplitude of the new point compared to the old point, and use this to rescale the wave so that the amplitude doesn't change
            scale=(1+weight)/2 
            newWave.append(int(temp/scale))
            
    return newWave

[waves,timing]=(waveSynth([20,1,20],[100,100,100],duration=1))

test=combineWaves(waves[1],waves[0],weight=0.1)
for dp in test:
    print(str(dp))



