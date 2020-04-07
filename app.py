from robolapse import *
import threading
import configparser as cp
import sys
from flask import Flask, escape, request, render_template

#Config
config = cp.ConfigParser()
config.read('config.ini')
# Config rail
DIR = config.getint('DEFAULT','DIR')
STEP = config.getint('DEFAULT','STEP')
SWITCH = config.getint('DEFAULT','SWITCH')
STEP_MODE = config.getint('DEFAULT','STEP_MODE') # 1 - full step; 2 - half microstep; 8 - 1/8 microstep; 16 - 1/16 microstep
SPAN = config.getfloat('DEFAULT','SPAN') #cm
SPAN_RATIO = config.getfloat('DEFAULT','SPAN_RATIO') #step/cm
# Config video
FRAME_RATE = config.getfloat('DEFAULT','FRAME_RATE') #frame/sec
VIDEO_LENGTH = config.getfloat('DEFAULT','VIDEO_LENGTH') #sec

rl = Robolapse()
rl.initialize()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move')
def move():
    return render_template('move.html')

@app.route('/api/rth', methods=['GET'])
def RTH():
    speed = request.args.get("speed")
    th = threading.Thread(target=rl.RTH, args=[float(speed)])
    th.daemon=True
    th.start()
    return "Returning to home at " + speed + " cm/min"

@app.route('/api/move', methods=['GET','POST'])
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

@app.route('/api/laps', methods=['GET'])
def LAPS():
    n = request.args.get("n")
    t = request.args.get("t")
    th = threading.Thread(target=rl.LAPS, args = [float(n),float(t)])
    th.daemon=True
    th.start()
    return "Performing " + n + " lap(s) in " + t + " min"

@app.route('/api/capture_tl', methods=['GET'])
def CAPTURE_TIMELAPSE():
    t = request.args.get("t", type=float)
    r = request.args.get("r", default=FRAME_RATE, type=float)
    vl = request.args.get("vl", default=VIDEO_LENGTH, type=float)
    op = request.args.get("override_period", default=False, type=bool)
    dt = request.args.get("dt", default=0.0, type=float)
    th = threading.Thread(target=rl.CAPTURE_TIMELAPSE, args = [t,r, vl, op,dt])
    th.daemon=True
    th.start()


if __name__ == '__main__':
    app.jinja_env.cache = {}
    app.run(debug=False, port=5000, host='0.0.0.0')
