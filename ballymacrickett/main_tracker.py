LORA_FREQUENCY = 434.250
# The callsign should be up to 6 characters
CALLSIGH = "BMCK1L"


# Make sure pigpiod is running
import os
os.system("sudo pigpiod")

from pytrack.tracker import *
from time import sleep

# Get the right smbus library (for i2c)
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bmp280 import BMP280

# Set up for the BMP280 sensor
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus, i2c_addr=0x77)

def extra_telemetry():
    # Add in the extra telemetry data from the bmp280 sensor (and round them to 2dp each)
    return "{},{}".format(round(bmp280.get_temperature(), 2), round(bmp280.get_pressure(), 2))


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
