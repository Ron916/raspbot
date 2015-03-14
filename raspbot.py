#Python version 3.2.3

import RPi.GPIO as io
import time

#ermagherrrddd no async out of teh box


class RaspBot:
    gpio = [12,16,21,19]

    def reset_lights(self):
        for val in self.gpio:
            io.output(val, False)

    def __init__(self):
        io.setmode(io.BCM)
        for val in self.gpio:
            io.setup(val, io.OUT)
        self.keyboard_loop()

    def keyboard_loop(self):
        key = ""
        while not(key == "q"):
            key = input("Command (q)uit (a) (r)eset: ")
            print(key)
            if key == 'a':
                self.loop_em()
            if key == 'r':
                self.reset_lights()

    def loop_em(self):
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




#array = ["Steve Perry", "Chuck Norris"]
#if array[0] > array[1]:
#    print("you're a towel")
#else:
#    print("what no wai")

#text = "?"
#while not(text == ""):
#    text = input("Type something: ")
#    print(text)
    
