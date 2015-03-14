#Python version 3.2.3

import RPi.GPIO as io
import time

class RaspBot:
    gpio = [12,16,21,19]

    @staticmethod
    def reset_lights():
        for val in gpio:
            io.output(val, False)

    def __init__(self):
        io.setmode(io.BCM)
        for val in gpio:
            io.setup(val, io.OUT)


    def one(self):
        self.reset_lights()
        count = 0
        while True:
            self.reset_lights()
            io.output(self.gpio[ count ], True)
            if count == 3:
                count = 0
            else:
                count = int(count) + 1
            time.sleep(.2)

pie = RaspBot()
pie.one()




#array = ["Steve Perry", "Chuck Norris"]
#if array[0] > array[1]:
#    print("you're a towel")
#else:
#    print("what no wai")

#text = "?"
#while not(text == ""):
#    text = input("Type something: ")
#    print(text)
    
