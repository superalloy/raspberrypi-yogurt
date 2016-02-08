#!/usr/bin/python

from w1thermsensor import W1ThermSensor
from Adafruit_CharLCD import Adafruit_CharLCD as LCD
from twilio.rest import TwilioRestClient

import time
import logging
import datetime
import RPi.GPIO as GPIO
import math
import threading
from config import *

sensor = W1ThermSensor()

logFN = time.strftime("logs/%Y-%m-%d_%H%M%S") + "_yPi_log.txt"

logging.basicConfig(filename=logFN, level=logging.DEBUG,
	format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
client = TwilioRestClient(account_sid, auth_token)

#GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd_cols = 16
lcd_rows = 2

hit_target = False

state_not_started = 1
state_pre_culture = 2
state_waiting_culture = 3
state_incubation = 4
state_done = 5
rampUpDown = 1 #1 is a ramp up temp, 2 is a ramp down temp

state = state_not_started
# Initialize the LCD using the pins above.
lcd = LCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_cols, lcd_rows, lcd_backlight)

# Print a two line message
lcd.message('Yogurt Pi')

def setTemp(T):
	global hit_target
	global finishTime
	if (temp_f < T):
		if (rampUpDown == 2):
			if (hit_target == False):
				hit_target = True
		#turn on the heater
#		print 'turn it on'
	else:
		if (rampUpDown == 1):
			if (hit_target == False):
				hit_target = True
				startTime = time.time()
				if (state == state_pre_culture):
					finishTime = startTime + time_1
				elif (state == state_incubation):
					finishTime = startTime + time_2
		#turn off the heater
#		print 'turn it off'
def sendTextMessage(msg):
	message = client.message.create(to=toText, from_=fromText, body=msg)

def startPreCulture(init_state):
	global rampUpDown
	global state
	global hit_target
	rampUpDown = 1
	hit_target = False
	state = state_pre_culture

def startWaitCulture():
	global rampUpDown
	global state
	global hit_target
	rampUpDown = 2
	hit_target = False
	state = state_waiting_culture

def startIncubation():
	global rampUpDown
	global state
	global hit_target
	rampUpDown = 1
	hit_target = False
	state = state_incubation

def endIncubation():
	print "done"
#	sendText("Yogurt is done")

def logData():
	threading.Timer(5.0, logData).start()
	logging.info('state: %s' % (state) + "\tT: %s" % (temp_f))

def getTimeRemaining(fTime):
	seconds = (fTime - time.time())
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	return ("%d:%02d:%02d" % (h, m, s), seconds)

logging.info('System starting, waiting for input')
while 1:
	button_state = GPIO.input(button_pin)
	temp_f = sensor.get_temperature(W1ThermSensor.DEGREES_F)
	if button_state == False:
		if state == state_not_started:
			logData()
			startPreCulture(state)
		elif (state == state_waiting_culture):
			#culture has been added
			startIncubation()
	if(state == state_not_started):
		lcd.clear()
		lcd.message('Press to start\n%s' % (temp_f))
		time.sleep(0.10)

	elif (state == state_pre_culture):
		setTemp(temp_1)
		if (hit_target == True):
			remaining = getTimeRemaining(finishTime)
			if (remaining[1] <=0):
				startWaitCulture()
		else:
			remaining = "wait", 0
		lcd.clear()
		lcd.message('GOAL: %s\n%s %s' % (temp_1, temp_f, remaining[0]))
		time.sleep(0.10)
	elif (state == state_waiting_culture):
		setTemp(temp_2)
		if (hit_target == True):
			lcd.clear()
			lcd.message('Add Culture\nPress Button')
		else:
			lcd.clear()
			lcd.message('GOAL: %s\n%s cooling' % (temp_2, temp_f))
	elif (state == state_incubation):
		setTemp(temp_2)
		if (hit_target == True):
			remaining = getTimeRemaining(finishTime)
			if (remaining[1] <= 0):
				endIncubation()
		else:
			remaining = "waiting", 0
		lcd.clear()
		lcd.message('GOAL: %s\n%s %s' % (temp_2, temp_f, remaining[0]))
		time.sleep(0.10)
