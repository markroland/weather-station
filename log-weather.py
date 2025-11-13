import serial
import http.client
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Configuration
# Load environment variables from .env file
load_dotenv()
serial_port = os.getenv("SERIAL_PORT", "/dev/ttyACM0")
domain = os.getenv("DOMAIN")
station_id = int(os.getenv("STATION_ID", "1"))

# Open serial connection
ser = serial.Serial(serial_port, 9600)

# Ensure the ./data directory exists
os.makedirs('./data', exist_ok=True)

# Open data file. Truncate. Use newline='' for CSV compatibility in Python 3
f = open('./data/data.csv', 'w', newline='', encoding='utf-8')

# Write header
f.write("Time,Humidity (%),Temp 1 (C),Temp 2 (F),Pressure (Pa),Light (V),V-in (V)\n")

# Read in and throw away 2 lines of the serial, which contain header information
# serial_line = ser.readline()
# serial_line = ser.readline()

# Do forever...
while True:

    try:
        # Get current time
        now = datetime.now()

        # Read from serial (decode bytes to str)
        serial_line = ser.readline().decode('utf-8').strip()

        # Set reading time
        reading_time = '{:%Y-%m-%d %H:%M:%S}'.format(now)

        # Define the data to log to
        line = "%s,%s\n" % (reading_time, serial_line.replace("\r", ""))

        f.write(line)
        f.flush()

        # Post to Weather Station API every minute
        if domain != "" and '{:%S}'.format(now) == "00":

            try:
                # Split comma-separated line of data
                line_parts = line.strip().split(',')

                # Create data object
                data = {
                    "station_id": station_id,
                    "log_time": line_parts[0],
                    "temperature": line_parts[3],
                    "humidity": line_parts[1],
                    "pressure": line_parts[4],
                    "light": line_parts[5],
                }

                http_body = json.dumps(data)
                http_headers = {"Content-type": "application/json"}
                conn = http.client.HTTPSConnection(domain, timeout=10)
                conn.request("POST", "/" + str(station_id), http_body, http_headers)
                response = conn.getresponse()
                # Read the response to ensure the connection can be reused
                response.read()
                # Optionally print or log response status
                # print(response.status, response.reason)
                conn.close()
            except Exception as e:
                # Log the error but continue running
                error_line = "%s,ERROR: %s\n" % (reading_time, str(e))
                f.write(error_line)
                f.flush()
                print(f"Error posting to server: {e}")
                # Ensure connection is closed even on error
                try:
                    conn.close()
                except:
                    pass

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        # Try to reconnect
        try:
            ser.close()
        except:
            pass
        time.sleep(5)
        try:
            ser = serial.Serial(serial_port, 9600)
        except Exception as reconnect_error:
            print(f"Failed to reconnect: {reconnect_error}")
            time.sleep(30)

    except Exception as e:
        print(f"Unexpected error in main loop: {e}")
        error_line = "%s,LOOP ERROR: %s\n" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(e))
        try:
            f.write(error_line)
            f.flush()
        except:
            pass

# Close file
f.close()

# Close serial connection
ser.close()
