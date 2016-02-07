#!/usr/bin/python

from w1thermsensor import W1ThermSensor
from Adafruit_CharLCD import Adafruit_CharLCD as LCD
import time
import logging
import datetime
import RPi.GPIO as GPIO
import math
sensor = W1ThermSensor()

logFN = time.strftime("logs/%Y-%m-%d_%H%M%S") + "_yPi_log.txt"

logging.basicConfig(filename=logFN, level=logging.DEGUG,
	format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Raspberry Pi pin configuration:
lcd_rs        = 27  # Note this might need to be changed to 21 for older revision Pisn
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = 4
button_pin 	= 5
#GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd_cols = 16
lcd_rows = 2

# initialize temp and time vars
temp_1 = 90
temp_2 = 110
time_1 = 600
time_2 = 28800 #8 hours in seconds

state_not_started = 1
state_pre_culture = 2
state_waiting_culture = 3
state_incubation = 4
state_done = 5

state = state_not_started
# Initialize the LCD using the pins above.
lcd = LCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_cols, lcd_rows, lcd_backlight)

dt = datetime.now()
data_run =
data_run = time.time()

# Print a two line message
lcd.message('Yogurt Pi')

def setTemp(T):
	if (temp_f < T):
		#turn on the heater
		print 'turn it on'
	else:
		#turn off the heate
		print 'turn it off'


def startPreCulture(init_state):
	startTime = time.time()
	global finishTime
	finishTime = startTime + time_1
	global state
	state = state_pre_culture

def logData:
	logging.info('state: %s' % (state) + "\tT: %s" % (temp_f))

while 1:
	temp_f = sensor.get_temperature(W1ThermSensor.DEGREES_F)
	button_state = GPIO.input(button_pin)
	logData()
	if button_state == False:
		if state == state_not_started:
			startPreCulture(state)

	if(state == state_not_started):
		lcd.clear()
		lcd.message('Press to start\nT: %sF, t: ' % (temp_f))
		time.sleep(0.10)

	elif (state == state_pre_culture):
		setTemp(temp_1)
		rem_min = (finishTime - time.time()) / 60
		rem_min = math.trunc(rem_min)
		rem_sec = (finishTime - time.time()) - 60*rem_min
		lcd.clear()
		lcd.message('Target: %s\nT:%sF;t:%s:%s' % (temp_1, temp_f,("{:.0f}".format(rem_min)), ("{0:02.0f}".format(rem_sec))))
		time.sleep(0.10)
