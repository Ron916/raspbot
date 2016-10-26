#Python version 2

print('flaskbot')

from flask import Flask, render_template, jsonify
from database import Database

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return render_template('raspbot.html')

@app.route('/raspbot/<string:command>/<string:value>', methods=['POST'])
def raspbot(command, value):
    return jsonify()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')