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

# Read in and throw away 2 lines of the serial, which contain header information
# serial_line = ser.readline()
# serial_line = ser.readline()

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

    # Post to Weather Station API every minute
    if '{:%S}'.format(now) == "00":

        # Split comma-separated line of data
        line_parts = line.split(',')

        # Create data object
        data = {
            "station_id" : 1,
            "log_time" : line_parts[0],
            "temperature" : line_parts[3],
            "humidity" : line_parts[1],
            "pressure" : line_parts[4],
            "light" : line_parts[5],
        }

        http_body = json.dumps(data)
        http_headers = {"Content-type": "application/json"}
        conn = httplib.HTTPConnection("project.markroland.com")
        conn.request("POST", "/weather-station/1", http_body, http_headers)
        response = conn.getresponse()

# Close file
f.close()

# Close serial connection
ser.close()
