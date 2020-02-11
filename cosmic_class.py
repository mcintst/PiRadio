#!/usr/bin/env python
# Raspberry Pi IQAudio Cosmic Controller Development Templates
# See IQAudio website at  http://iqaudio.co.uk
#
# Raspberry Pi Cosmic Controller (IQAudio) Class
# $Id: cosmic_class.py,v 1.2 2018/05/15 09:38:36 bob Exp $
#
# Author: Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This class uses one standard rotary encoder with push switch
# and three push to make buttons. It also has three status LEDs and option IR sensor
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#            The authors shall not be liable for any loss or damage however caused.
#
#

import os,sys,pwd
import time,pdb
import RPi.GPIO as GPIO
from config_class import Configuration

config = Configuration()

class Button:

	# Default configuration left to right
	left_switch = 4
	middle_switch = 5
	right_switch = 6

	# Rotary encoder
	encoder_switch = 27
	encoder_a = 23
	encoder_b = 24

	# Status LEDs
	led1 = 14
	led2 = 15
	led3 = 16

	def __init__(self,button,callback):
		self.button = button
		self.callback = callback

		if self.button > 0:
			GPIO.setmode(GPIO.BCM)
			GPIO.setwarnings(False)

			try:
				# The following lines enable the internal pull-up resistor
				GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

				# Add event detection to the GPIO inputs
				GPIO.add_event_detect(self.button, GPIO.FALLING, 
							callback=self.button_event,
							bouncetime=200)
			except Exception as e:
				print("Button GPIO {} initialise error: {}".format(str(self.button),str(e)))
				sys.exit(1)
		 

	# Push button event
	def button_event(self,button):
		event_button = self.button
		self.callback(event_button)	# Pass button event to event class
		return

	# Was a button pressed (goes from 1 to 0)
	def pressed(self):
		state = GPIO.input(self.button)
		if state == 0:
			pressed = True
		else:
			pressed = False
		return pressed

# End of Cosmic Button Class
