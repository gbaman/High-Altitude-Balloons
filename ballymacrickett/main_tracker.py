LORA_FREQUENCY = 434.250
# The callsign should be up to 6 characters
CALLSIGH = "BMCK1L"


# Make sure pigpiod is running
import os
os.system("sudo pigpiod")

from pytrack.tracker import *
from time import sleep
from w1thermsensor import W1ThermSensor

# Get the right smbus library (for i2c)
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bmp280 import BMP280

# Set up for the BMP280 sensor
try:
    bus = SMBus(1)
    bmp280 = BMP280(i2c_dev=bus, i2c_addr=0x77)
except:
    print("------------- NO BMP sensor!! -------------")
    bmp280 = None
 
try:
    temp_sensor = W1ThermSensor()
    t = temp_sensor.get_temperature()
except:
    print("------------- NO temp sensor!! -------------")
    temp_sensor = None

def extra_telemetry():
    # Add in the extra telemetry data from the bmp280 sensor (and round them to 2dp each)
    if temp_sensor:
        w_temp = round(temp_sensor.get_temperature(), 2)
    else:
        w_temp = 300
    if bmp280:
        bmp_temp = round(bmp280.get_temperature(), 2)
        bmp_pressure = round(bmp280.get_pressure(), 2)
    else:
        bmp_temp = 100
        bmp_pressure = 200

    batt_voltage = 0

    return "{},{},{},{}".format(bmp_temp, bmp_pressure, w_temp, batt_voltage)


payload = Tracker()
payload.set_sentence_callback(extra_telemetry)

# Setup LoRa
payload.set_lora(payload_id=CALLSIGH , channel=1, frequency=LORA_FREQUENCY, mode=1)

# Add the LoRA camera schedule and also save the full images
payload.add_lora_camera_schedule('images/LORA', period=60)
payload.add_full_camera_schedule('images/FULL', period=60, width=3280, height=2464)

payload.start()

# Don't let the program die...
while True:
    sleep(1)
