#This program generates a constant vibration at specified frequency
#You can adjust the frequency in Hz by setting the freq variable
freq=20
secondsOn=(1/freq)/2
vibeArray=[[100,0],[100,0],[100,0]]
timing=[secondsOn,secondsOn]
vibePattern(vibeArray,timing,loop=90000)

