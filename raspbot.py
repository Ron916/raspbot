#Python version 3.2.3

import RPi.GPIO as io
import time
from flask import Flask, render_template, jsonify


class RaspBot:
    gpio = [20,21,22,23,24,25,26,27]
    timeout = 0.2
    max_loops = 10

    def cli_loop(self):
        self.keyboard_loop()

    def all_off(self):
        for val in self.gpio:
            io.output(val, False)

    def all_on(self):
        for val in self.gpio:
            io.output(val, True)

    def __init__(self):
        io.setmode(io.BCM)
        for val in self.gpio:
            io.setup(val, io.OUT)

    def keyboard_loop(self):
        key = ""
        while not(key == "q"):
            key = input("Command (q)uit (l)oop (a)ll (o)ff (r)eset (f)orward (b)ackward (1)BackAndForth (2)LoopForward (3)LoopBackward (4)BackForthEven (5)BackForthOdd: ")
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
        for x in range(1, self.max_loops):
            self.run_forward(type)    

    def loop_backward(self, type = 'all'):
        self.all_off()
        for x in range(1, self.max_loops):
            self.run_backward(type)	

    def back_forth(self, type = 'all'):
        self.all_off()
        for x in range(1, self.max_loops):
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



app = Flask(__name__)
raspBot = RaspBot()

@app.route('/', methods=['GET'])
def main():
    return render_template('raspbot.html')

@app.route('/raspbot/<string:command>/<string:value>', methods=['POST'])
def raspbot(command, value):
    if command == 'loop':
        if value == 'forward':
            raspBot.loop_forward()
        if value == 'backward':
            raspBot.loop_backward()
    return jsonify(errors=False)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')