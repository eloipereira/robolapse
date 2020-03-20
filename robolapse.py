from time import sleep
import RPi.GPIO as gpio
import math

DIR = 20
STEP = 21
CW = 1
CCW = 0
SWITCH = 12
excit_mode = 16.0
span = 70 #cm
span_ratio = 50 #step/cm

length = span * span_ratio * excit_mode
speed1 = 1/0.0005
speed2 = 1/0.001

gpio.setmode(gpio.BCM)
gpio.setup(DIR,gpio.OUT)
gpio.setup(STEP,gpio.OUT)
gpio.setup(SWITCH,gpio.IN,pull_up_down=gpio.PUD_UP)
gpio.output(DIR,CW)

#GOTO - go to a specific location (normalized to the total length) 
def GOTO(location,speed=70.0):
        RTH(speed)
	delta_t = 60.0 / (speed * span_ratio * excit_mode) - (excit_mode * 2.0/3.0 - 2.0/3.0)/length
        try:
                sleep(1)
                direction = CW
                for l in range(int(math.floor(location*length))):
                        gpio.output(DIR,direction)
			gpio.output(STEP,gpio.HIGH)
			sleep(delta_t/2.0)
			gpio.output(STEP,gpio.LOW)
			sleep(delta_t/2.0)
                        if (l+1)%length == 0:
                                direction = (direction + 1)%2
        except KeyboardInterrupt:
                print("Stop!")
                gpio.cleanup()
        

# RTH - Return to home 
def RTH(speed=70.0):
	delta_t = 60.0 / (speed * span_ratio * excit_mode) - (excit_mode * 2.0/3.0 - 2.0/3.0)/length
	try:
		if gpio.input(SWITCH) == False:
			at_home = True
		else:
			at_home = False
		sleep(1)
		while not at_home:
			gpio.output(DIR,CCW)
			gpio.output(STEP,gpio.HIGH)
			sleep(delta_t/2.0)
			gpio.output(STEP,gpio.LOW)
			sleep(delta_t/2.0)
			if gpio.input(SWITCH) == False:
				at_home = True
                sleep(1)
                while at_home:
			gpio.output(DIR,CW)
			gpio.output(STEP,gpio.HIGH)
			sleep(delta_t/2.0)
			gpio.output(STEP,gpio.LOW)
			sleep(delta_t/2.0)
			if gpio.input(SWITCH) == True:
				at_home = False

	except KeyboardInterrupt:
		print("Stop!")
		gpio.cleanup()
                

GOTO(1,70.0)
