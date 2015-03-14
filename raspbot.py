#Python version 3.2.3

import RPi.GPIO as io
import time

io.setmode(io.BCM)

gpio = [12,16,21,19]
for val in gpio:
    io.setup(val, io.OUT)

def resetLights():
    for val in gpio:
        io.output(val, False)

def one():
    yey = True
    resetLights()
    count = 0
    while True:
        resetLights()
        io.output(gpio[ count ], True)
        if count == 3:
            count = 0
        else:
            count = int(count) + 1
        time.sleep(.2)

one()
    
        



#array = ["Steve Perry", "Chuck Norris"]
#if array[0] > array[1]:
#    print("you're a towel")
#else:
#    print("what no wai")

#text = "?"
#while not(text == ""):
#    text = input("Type something: ")
#    print(text)
    
