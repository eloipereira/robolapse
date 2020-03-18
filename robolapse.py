from time import sleep
import RPi.GPIO as gpio

DIR = 20
STEP = 21
CW = 1
CCW = 0
excit_mode = 1

lenght = 3500 * excit_mode
speed1 = 1/0.0005
speed2 = 1/0.001

gpio.setmode(gpio.BCM)
gpio.setup(DIR,gpio.OUT)
gpio.setup(STEP,gpio.OUT)
gpio.output(DIR,CW)

try:
	while True:
		sleep(1)
		gpio.output(DIR,CW)
		for x in range(lenght):
			gpio.output(STEP,gpio.HIGH)
			sleep(1/speed1)
			gpio.output(STEP,gpio.LOW)
			sleep(1/speed1)

		sleep(1)
		gpio.output(DIR,CCW)
		for x in range(lenght):
			gpio.output(STEP,gpio.HIGH)
			sleep(1/speed2)
			gpio.output(STEP,gpio.LOW)
			sleep(1/speed2)

except KeyboardInterrupt:
	print("Stop!")
	gpio.cleanup()
