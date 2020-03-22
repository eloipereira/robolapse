import robolapse as rl
from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Robolapse app!"

@app.route('/api/rth', methods=['GET'])
def RTH():
    speed = request.args.get("speed")
    rl.RTH(float(speed))
    return "Return to home completed"

@app.route('/api/goto', methods=['GET'])
def GOTO():
    loc = request.args.get("location")
    speed = request.args.get("speed")
    rl.GOTO(float(loc),float(speed))
    return "GOTO completed"

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
