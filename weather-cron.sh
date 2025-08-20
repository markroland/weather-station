#!/bin/sh

# Check to see if the script "~/Documents/Projects/weather-station/log-weather.py"
# is running. If it isn't, then start it.

if ! pgrep -f "python ./log-weather.py" > /dev/null
then
    cd ~/Documents/Projects/weather-station && nohup python ./log-weather.py > log.txt 2>&1 &
    # echo "Started"
# else
    # echo "Running"
fi
