from random import choice

while True:
    freq=choice([5,10,15])
    secondsOn=(1/freq)/2
    loopNum=(10//choice)
    vibeArray=[[100,0],[100,0],[100,0]]
    timing=[secondsOn,secondsOn]
    send(str(time.time()+","+str(freq)))
    vibePattern(vibeArray,timing,loop=loopNum)
    nullArray=[[0,0],[0,0],[0,0]]
    vibePattern(nullArray,timing,loop=loopNum)
         
