#!/usr/bin/env python
#
# Measure light levels using a photoresistor and capacitor and log to web
#
# Usage: cd ~/Documents/Projects/Weather && nohup python ./log-light.py > log-light.log 2>&1 &
#
# 3/31/2017 - Created

import time
import httplib
import json
from datetime import datetime
import RPi.GPIO as GPIO

# Open data file. Truncate. Don't buffer.
f = open('./data/station-2.csv', 'w', 0)

# Write header
f.write("Time,Light\n")

# Turn off "channel is already in use" warning
GPIO.setwarnings(False)

# Set the pin identification method
GPIO.setmode(GPIO.BCM)

# Function: Measure capacitor charging time
def RCtime (RCpin):

    # Intialize reading flag to "off"
    reading = 0

    # Configure pin as output
    GPIO.setup(RCpin, GPIO.OUT)

    # Drive output voltage low and wait for signal to settle
    GPIO.setup(RCpin, GPIO.LOW)
    time.sleep(0.1)

    # Configure pin as an input
    GPIO.setup(RCpin, GPIO.IN)

    # Read the GPIO pin until it goes high
    while (GPIO.input(RCpin) == GPIO.LOW):
            reading += 1
    return reading

# Do forever...
while 1:

    # Get current time
    now = datetime.now()

    # Set reading time
    reading_time = '{:%Y-%m-%d %H:%M:%S}'.format(now)

    # Post to Weather Station API every minute
    if '{:%S}'.format(now) == "00":

        # Measure the light level
        light_level = RCtime(18)

        # Log data to file
        line = "%s,%s\n" % (reading_time, light_level)
        f.write(line)

        # Create data object
        data = {
            "station_id" : 2,
            "log_time" : reading_time,
            "light" : light_level / 100000.0,
        }

        http_body = json.dumps(data)
        http_headers = {"Content-type": "application/json"}
        conn = httplib.HTTPConnection("project.markroland.com")
        conn.request("POST", "/weather-station/2", http_body, http_headers)
        response = conn.getresponse()

        # Sleep for 1 second so that multiple HTTP requests will not be made
        time.sleep(1)

# Close file
f.close()
