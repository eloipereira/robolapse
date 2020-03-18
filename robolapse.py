from time import sleep
import RPi.GPIO as gpio

DIR = 20
STEP = 21
CW = 1
CCW = 0
SWITCH = 12
excit_mode = 1

lenght = 3500 * excit_mode
speed1 = 1/0.0005
speed2 = 1/0.001

gpio.setmode(gpio.BCM)
gpio.setup(DIR,gpio.OUT)
gpio.setup(STEP,gpio.OUT)
gpio.setup(SWITCH,gpio.IN,pull_up_down=gpio.PUD_UP)
gpio.output(DIR,CW)

# Return to home function
def RTH(speed=500):
	try:
		if gpio.input(SWITCH) == False:
			at_home = True
		else:
			at_home = False

		while not at_home:
			gpio.output(DIR,CCW)
			gpio.output(STEP,gpio.HIGH)
			sleep(1/speed)
			gpio.output(STEP,gpio.LOW)
			sleep(1/speed)
			if gpio.input(SWITCH) == False:
				at_home = True

	except KeyboardInterrupt:
		print("Stop!")
		gpio.cleanup()

RTH()
