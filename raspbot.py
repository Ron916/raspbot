#Python version 2

print('raspbot')

import RPi.GPIO as io
import time
from database import Database


class RaspBot:
    gpio = [20,21,22,23,24,25,26,27]
    timeout = 0.2
    max_loops = 10
    loop = True

    def all_off(self):
        self.loop = False
        for val in self.gpio:
            io.output(val, False)

    def all_on(self):
        for val in self.gpio:
            io.output(val, True)

    def __init__(self):
        io.setmode(io.BCM)
        for val in self.gpio:
            io.setup(val, io.OUT)

    def cli_loop(self):
        key = ""
        while not(key == "q"):
            key = raw_input("Command (q)uit (l)oop (a)ll (o)ff (r)eset (f)orward (b)ackward (1)BackAndForth (2)LoopForward (3)LoopBackward (4)BackForthEven (5)BackForthOdd: ")
            if key == 'l':
                self.loop_em()
            if key == 'a':
                self.all_on()
            if key == 'o':
                self.all_off()
            if key == 'f':
                self.run_forward()
            if key == 'b':
                self.run_backward()
            if key == '1':
                self.back_forth()
            if key == '2':
                self.loop_forward()
            if key == '3':
                self.loop_backward()
            if key == '4':
                self.back_forth('even')
            if key == '5':
                self.back_forth('odd')

    def loop_forward(self, type = 'all'):
        self.all_off()
        self.loop = True
        while self.loop:
            self.run_forward(type)    

    def loop_backward(self, type = 'all'):
        self.all_off()
        self.loop = True
        while self.loop:
            self.run_backward(type)	

    def back_forth(self, type = 'all'):
        self.all_off()
        self.loop = True
        while self.loop:
            self.run_forward(type)
            self.run_backward(type)

    def run_forward(self, type = 'all'):
        for var in self.gpio:
            if (type == 'even') and (var % 2 == 0):
                continue
            if (type == 'odd') and (not(var % 2 == 0)):
                continue
            io.output(var, True)
            time.sleep(self.timeout)
            io.output(var, False)
        
    def run_backward(self, type = 'all'):
        for var in reversed(self.gpio):
            if (type == 'even') and (var % 2 == 0):
                continue
            if (type == 'odd') and (not(var % 2 == 0)):
                continue
            io.output(var, True)
            time.sleep(self.timeout)
            io.output(var, False)

if __name__ == '__main__':
    raspBot = RaspBot()
    while True:
        # this loop will check the database for a command and update the raspbot
        # maybe have it query the database twice per second?
        pass
