#!/usr/bin/env python3
#
# script to run raspberry pi as Internet Radio using the IQAudio Pi-DACZero and the IQAudio Cosmic Controller
# read in the URLs for each of the streams and toggle through them using the rotary encoder
# play the streams with mplayer
# display the current radio station on the display
#

# Based on the following template:
# Raspberry Pi IQAudio Cosmic Controller Development Templates
# See IQAudio website at  http://iqaudio.co.uk
#
# Raspberry Pi Cosmic Controller (IQAudio) Class
# $Id: test_controller.py,v 1.6 2018/05/27 09:43:07 bob Exp $
#
# Author: Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This class uses one standard rotary encoder with push switch
# and three push to make buttons. It also has three status LEDs and option IR sensor
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#	    The authors shall not be liable for any loss or damage however caused.
#

import sys,os,pwd
import time
import ast
import subprocess

if "/usr/share/cosmicd" not in sys.path:
	sys.path.append("/usr/share/cosmicd")
from rotary_class import RotaryEncoder
from status_led_class import StatusLed
from config_class import Configuration
from cosmic_class import Button

config = Configuration()

### Test routines ###
left_switch = 0
middle_switch = 0
right_switch = 0
encoder_switch = 0
encoder_a = 0
encoder_b = 0

statusLed = None
Names = ['NO_EVENT', 'CLOCKWISE', 'ANTICLOCKWISE', 'BUTTON DOWN', 'BUTTON UP']

def button_event(gpio):
	global encoder_switch,left_switch,middle_switch
	print("Button pressed on GPIO, {}".format(gpio))

	statusLed.clear()
	if gpio == left_switch:
		statusLed.set(StatusLed.LED1,True)
	elif gpio == middle_switch:
		statusLed.set(StatusLed.LED2,True)
	elif gpio == right_switch:
		statusLed.set(StatusLed.LED3,True)
	return

# Test only - No event sent
def rotary_event(event):
	name = ''
	try:
	        name = Names[event]
	except:
	        name = 'ERROR'

	global current_radio_station_index
	global max_radio_station_index
	statusLed.clear()
	if event == RotaryEncoder.CLOCKWISE:
		statusLed.set(StatusLed.LED3,True)
		current_radio_station_index = current_radio_station_index + 1
		if (current_radio_station_index > max_radio_station_index):
			current_radio_station_index = 0
	elif event == RotaryEncoder.ANTICLOCKWISE:
		statusLed.set(StatusLed.LED1,True)
		current_radio_station_index = current_radio_station_index - 1
		if (current_radio_station_index < 0):
			current_radio_station_index = max_radio_station_index
	else:
		# Handle button up/down
	        statusLed.clear()

	print("Rotary event {}, {}".format(event,name))
	print("current_radio_station_index {}".format(current_radio_station_index))
	global proc	
	global radio_station_list	

# try and stop any currently running mplayer process	
	try:
		stop_audio_stream(proc)
	except NameError:
		pass
	proc = start_audio_stream(radio_station_list[current_radio_station_index])	
	return

# Configure status LED
def statusLedInitialise(statusLed):
	led1 = config.getLed1()
	led2 = config.getLed2()
	led3 = config.getLed3()
	statusLed = StatusLed(led1,led2,led3)
	print("statusLed,{},{},{}".format(led1,led2,led3))
	return statusLed

# Read in the list of Radio Stations and their URLS
def read_radio_stations():
	radio_station_list = []
	temp_tuple = []
	f = open("radio_streams.txt","r")
	for each_line in f:
		if each_line[0] == "\"":
			temp_array = each_line.rstrip().split(",")
# remove the leading quotes and add to the tuple
			temp_tuple.append(temp_array[0][1:])
# add the rest of the array to the tuple

			temp_tuple.append(temp_array[1:])
			radio_station_list.append(temp_tuple[:])
			temp_tuple.clear()
		next				

	return radio_station_list

# Start an audio stream
def start_audio_stream(radio_station_tuple):
	subprocess_command = ["/usr/bin/mplayer","-really-quiet","-nolirc","-ao","alsa:device=hw=0,0"]
	subprocess_command = subprocess_command + radio_station_tuple[1]
	#print(subprocess_command)
	proc = subprocess.Popen(subprocess_command)
	return proc

def stop_audio_stream(proc):
	try:	
		print("About to kill PID:{}".format(proc.pid))
		proc.terminate()
		outs, errs = proc.communicate()
		print("outs: {}".format(outs))
		print("errs: {}".format(errs))

#	except TimeoutExpired:
#		print("TimeoutExpired")
	except:
		print("Unexpected error: {}".format(sys.exc_info()[0]))
		raise

	return

if __name__ == "__main__":

	radio_station_list = read_radio_stations()	
	max_radio_station_index = len(radio_station_list)-1
	current_radio_station_index = 0
#	print(radio_station_list)
	proc = start_audio_stream(radio_station_list[current_radio_station_index])
	print("PID: {}".format(proc.pid))

	print("Test Cosmic Controller Class")
	print("============================")

	# Get configuration
	left_switch = config.getLeftSwitch()
	middle_switch = config.getMiddleSwitch()
	right_switch = config.getRightSwitch()
	encoder_switch = config.getEncoderSwitch()
	encoder_a = config.getEncoderA()
	encoder_b = config.getEncoderB()

	print("Left switch GPIO {}".format(left_switch))
	print("Middle switch GPIO {}".format(middle_switch))
	print("Right switch GPIO {}".format(right_switch))
	print("Encoder A GPIO {}".format(encoder_a))
	print("Encoder B GPIO {}".format(encoder_b))
	print("Encoder switch GPIO {}".format(encoder_switch))

	Button(left_switch, button_event)
	Button(middle_switch, button_event)
	Button(right_switch, button_event)

	rotaryknob = RotaryEncoder(encoder_a,encoder_b,encoder_switch,rotary_event)

	statusLed = statusLedInitialise(statusLed)
	statusLed.set(StatusLed.LED1,True)
	time.sleep(1)
	statusLed.clear()
	statusLed.set(StatusLed.LED2,True)
	time.sleep(1)
	statusLed.clear()
	statusLed.set(StatusLed.LED3,True)
	time.sleep(1)
	statusLed.clear()
	time.sleep(1)

	# Main wait loop
	try:
		while True:
			time.sleep(0.2)

	except KeyboardInterrupt:
		print(" Stopped")
		sys.exit(0)

	# End of script

