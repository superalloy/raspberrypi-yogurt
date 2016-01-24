# raspberrypi-yogurt
A raspberry pi based yogurt maker.

The device uses a DS18B20 waterproof temperature sensor and a main power relay to manage the temperature of a slow cooker. The device uses a 16x2 LCD to display the current state and it uses Twilio to send an SMS message when the yogurt is done and ready for refrigeration.

If you want to use the SMS feature, you will need a Twilio.com account, I use a free trial account because I'm only using the twilio account to send messages to myself. The account gives you the ability to send an SMS message when the yogurt finishes it's incubation cycle.

An image of the connections will be inserted here. (once it's done)

The pin out of the Raspberry Pi is:
* GPIO 04: TEMP SENSOR DATA (Orange Wire)
* GPIO 05: D6 (LCD PIN 13)
* GPIO 06: D5 (LCD PIN 12)
* GPIO 11: D7 (LCD PIN 14)
* GPIO 13: D4 (LCD PIN 11)
* GPIO 19: ENABLE (LCD PIN 6)
* GPIO 23: RELAY-ON
* GPIO 26: RS (LCD PIN 4)

