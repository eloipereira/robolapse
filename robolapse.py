from time import sleep
import RPi.GPIO as gpio
import math

DIR = 20
STEP = 21
CW = 1
CCW = 0
SWITCH = 12
excit_mode = 16 # 1 - full step; 2 - half microstep; 8 - 1/8 microstep; 16 - 1/16 microstep
span = 70 #cm
span_ratio = 50 #step/cm

length = span * span_ratio * excit_mode
gpio_is_set = False

def setup_gpio():
	global gpio_is_set
	if not gpio_is_set:
		gpio.setmode(gpio.BCM)
		gpio.setup(DIR,gpio.OUT)
		gpio.setup(STEP,gpio.OUT)
		gpio.setup(SWITCH,gpio.IN,pull_up_down=gpio.PUD_UP)
		gpio.output(DIR,CW)
		gpio_is_set = True

#GOTO - go to a specific location (normalized to the total length)
def GOTO(location,speed=70.0):
	global gpio_is_set
	setup_gpio()
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
		gpio_is_set = False


# RTH - Return to home
def RTH(speed=70.0):
	global gpio_is_set
	setup_gpio()
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
		gpio_is_set = False
