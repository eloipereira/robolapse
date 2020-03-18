from time import sleep
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(12,gpio.IN,pull_up_down=gpio.PUD_UP)

try:
	while True:
		input_state=gpio.input(12)
		if input_state == False:
			print("button pressed")
			sleep(0.2)

except KeyboardInterrupt:
	gpio.cleanup()
