# Weather Station

This project uses the SparkFun Weather Shield with an Arduino microcontroller to measure
atmospheric temperature, pressure, humidity and light.

# Resources

## Parts

 - Arduino Uno (Revision 3)
 - [SparkFun Weather Shield](https://www.sparkfun.com/products/12081)
 - [Stackable Headers](https://www.sparkfun.com/products/11417)
 - Raspberry Pi 3 (Model B v1.2)
   - Running Raspbian GNU/Linux 8 (jessie)
   - Requires Python 2.7
 - Power Supply for Raspberry Pi
 - USB Cable (Type A Male to Type B Male)

## Tools

 - Solder
 - Soldering Iron 

## Software

 - [Arduino IDE](https://www.arduino.cc/en/Main/Software)

## Source Code

 - [Sparkfun Github Weather Shield Repository](https://github.com/sparkfun/Weather_Shield) (Commit 4c92106 from 6/10/2016)

# Setup

1) Assemble the Weather Shield. Instructions may be found at
[https://learn.sparkfun.com/tutorials/weather-shield-hookup-guide](https://learn.sparkfun.com/tutorials/weather-shield-hookup-guide).

2) Download the "Weather Shield Basic" Arduino sketch from the
[Sparkun Repository](https://github.com/sparkfun/Weather_Shield/tree/master/firmware/Weather_Shield_Basic)
and upload it to the Arduino Uno.

3) Set up the external web server

4) Run the Python script on the Raspberry Pi to post the data to the external web server

    A) Determine the Serial device name/port (e.g. /dev/ttyACM0). Typically the device will be
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

    B) Start script

```
python ./log-weather.py
```

# License

[Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
