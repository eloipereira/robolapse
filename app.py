import robolapse as rl
import threading
from flask import Flask, escape, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/rth', methods=['GET'])
def RTH():
    speed = request.args.get("speed")
    th = threading.Thread(target=rl.RTH, args=[float(speed)])
    th.daemon=True
    th.start()
    return "Returning to home at " + speed + " cm/min"

@app.route('/api/goto', methods=['GET'])
def GOTO():
    loc = request.args.get("location")
    speed = request.args.get("speed")
    th = threading.Thread(target=rl.GOTO, args = [float(loc),float(speed)])
    th.daemon=True
    th.start()
    return "Going to " + loc + " cm at " + speed + " cm/min"

@app.route('/api/move', methods=['GET'])
def MOVE():
    length = request.args.get("length")
    speed = request.args.get("speed")
    direction = request.args.get("direction")
    if direction == "right":
        dir = 0
    elif direction == "left":
        dir = 1
    th = threading.Thread(target=rl.MOVE, args = [float(length),float(speed),dir])
    th.daemon=True
    th.start()

    return "Moving " + length + " cm to the " + direction + " at " + speed + " cm/min"

if __name__ == '__main__':
    app.jinja_env.cache = {}
    app.run(debug=False, port=80, host='0.0.0.0')
