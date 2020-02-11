#!/usr/bin/env python
# Raspberry Pi IQAudio Cosmic Controller Development Templates
# See IQAudio website at  http://iqaudio.co.uk
#
# $Id: status_led_class.py,v 1.4 2018/05/18 08:17:51 bob Exp $
# IQAudio Cosmic Controller LED
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#

import RPi.GPIO as GPIO
import time


# Status LED class
class StatusLed:
	led1 = None
	led3 = None
	led2 = None

	LED1 = 1
	LED2 = 2
	LED3 = 3

	# The init routine uses default GPIO settings
	def __init__(self, led1=23, led2=27, led3=22 ):
		self.led1 = led1
		self.led2 = led2
		self.led3 = led3

		# Set up status LEDS
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		if self.led1 > 0:
			GPIO.setup(self.led1, GPIO.OUT)
		if self.led2 > 0:
			GPIO.setup(self.led2, GPIO.OUT)
		if self.led3 > 0:
			GPIO.setup(self.led3, GPIO.OUT)
		return

	# Set the status to normal, busy, error or clear
	def set(self,led,onoff):
		# onoff is True or False
		if led == self.LED1:
			GPIO.output(self.led1, onoff)
		elif led == self.LED2:
			GPIO.output(self.led2, onoff)
		elif led == self.LED3:
			GPIO.output(self.led3, onoff)
		return 

	# Switch all LEDs off
	def clear(self):
		GPIO.output(self.led1, False)
		GPIO.output(self.led2, False)
		GPIO.output(self.led3, False)
		return 

if __name__ == "__main__":
	statusLed = StatusLed()
	statusLed.set(StatusLed.NORMAL)
	time.sleep(3)
	statusLed.set(StatusLed.BUSY)
	time.sleep(3)
	statusLed.set(StatusLed.ERROR)
	time.sleep(3)
	statusLed.set(StatusLed.CLEAR)

# End of class
