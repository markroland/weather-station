import serial
import httplib
import json
from datetime import datetime

# Open serial connection
ser = serial.Serial('/dev/ttyACM1', 9600)

# Open data file. Truncate. Don't buffer.
f = open('./data/data.csv', 'w', 0)

# Write header
f.write("Time,Humidity (%),Temp 1 (C),Temp 2 (F),Pressure (Pa),Light (V),V-in (V)\n")

# Do forever...
while 1:

    # Get current time
    now = datetime.now()

    # Read from serial
    serial_line = ser.readline()

    # Set reading time
    reading_time = '{:%Y-%m-%d %H:%M:%S}'.format(now)

    # Define the data to log to
    line = "%s,%s" % (reading_time, serial_line.replace("\r",""))

    f.write(line)

# Close file
f.close()

# Close serial connection
ser.close()
