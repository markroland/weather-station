# Weather Station

This project uses the SparkFun Weather Shield with an Arduino microcontroller to measure
atmospheric temperature, pressure, humidity and light.

## Parts

 - Arduino Uno (Revision 3)
 - [SparkFun Weather Shield](https://www.sparkfun.com/products/12081)
 - [Stackable Headers](https://www.sparkfun.com/products/11417)
 - Raspberry Pi 3 (or newer)
   - Raspberry Pi OS
   - Python 3
 - Power Supply for Raspberry Pi
 - USB Cable (Type A Male to Type B Male)

## Tools

 - Solder
 - Soldering Iron 

## Software

 - [Arduino IDE](https://www.arduino.cc/en/Main/Software)

## Source Code

 - [Sparkfun Github Weather Shield Repository](https://github.com/sparkfun/Weather_Shield) (Commit 4c92106 from 6/10/2016)

## Setup

1) Assemble the Weather Shield. Instructions may be found at
[https://learn.sparkfun.com/tutorials/weather-shield-hookup-guide](https://learn.sparkfun.com/tutorials/weather-shield-hookup-guide).

2) Download the "Weather Shield Basic" Arduino sketch from the
[Sparkun Repository](https://github.com/sparkfun/Weather_Shield/tree/master/firmware/Weather_Shield_Basic)
and upload it to the Arduino Uno.

3) Run the logging script from the Raspberry Pi

```
python ./log-weather.py
```

**Optional: Customize the .env**

Determine the Serial device name/port (e.g. /dev/ttyACM0). Typically the device will be
"/dev/ttyACM" followed by an integer in the order for which the device was attached, starting
with zero. So for example, if it was the first USB device attached, then the name would be
"/dev/ttyACM0".

```sh
ls /dev/tty*
```

OR

```sh
dmesg | grep tty
```

The default value used in the script is /dev/ttyACM0 so if your serial port
is different then define this SERIAL_PORT value in the .env file.

4) Optional: Set up the external web server to receive logging

An external web server can be set up to receive logging data in real time.
This is currently hosted in a private repository at https://github.com/markroland/weather-station-client. To use this feature, set up the server as instructed
in the repository and then copy .env.example to .env and customize it for the
remote server.

## Run in the background

To run the logger in the background you can SSH into your Raspberry Pi and run:

```
nohup python ./log-weather.py > log.txt 2>&1 &
```

This command runs the `log-weather.py` script in the background, even after you log out or disconnect from the terminal. It uses `nohup` to ignore hangup signals, redirects all output (both standard output and errors) to `log.txt`, and the trailing `&` puts the process in the background. This way, the script continues logging data without needing an active terminal session.

## Automation

If you want to the script to run on startup then you can add the `weather-cron.sh`
script to your crontab. Be sure to update the project path

## License

[Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
