#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os.path
import re
import sys
import os
from time import sleep
from time import gmtime, strftime
import numpy as np
import datetime
import subprocess
import base64
import uuid
import datetime
import traceback
import math
import random, string
import socket
import base64
import json
import math
import time
import psutil
import socket
from time import gmtime, strftime
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
#
# Sensors
#
from bh1745 import BH1745
from ltr559 import LTR559
import VL53L1X
import ltr559
import bme680
from lsm303d import LSM303D
import pulsar
import logging
from pulsar.schema import *
from pulsar.schema import AvroSchema
from pulsar.schema import JsonSchema
from pulsar import Client, AuthenticationOauth2

### 
#https://pulsar.apache.org/docs/en/client-libraries-python/
# http://pulsar.apache.org/api/python/schema/schema.m.html#pulsar.schema.schema.AvroSchema 
class breakoutsensor(Record):
    uuid = String()
    ipaddress = String()
    cputempf = Integer()
    runtime = Integer()
    host = String()
    hostname = String()
    macaddress = String()
    endtime = String()
    te = String()
    cpu = Float()
    diskusage = String()
    memory = Float()
    rowid = String()
    systemtime = String()
    ts = Integer()
    starttime = String()
    BH1745_red = Float()
    BH1745_green = Float()
    BH1745_blue = Float()
    BH1745_clear = Float()
    VL53L1X_distance_in_mm = Float()
    ltr559_lux = Float()
    ltr559_prox = Float()
    bme680_tempc = Float()
    bme680_tempf = Float()
    bme680_pressure = Float()
    bme680_humidity = Float()
    lsm303d_accelerometer = String() 
    lsm303d_magnetometer = String() 

# parse arguments
parse = argparse.ArgumentParser(prog='breakoutsensor.py')
parse.add_argument('-su', '--service-url', dest='service_url', type=str, required=True,
                   help='The pulsar service you want to connect to')
parse.add_argument('-t', '--topic', dest='topic', type=str, required=True,
                   help='The topic you want to produce to')
parse.add_argument('-n', '--number', dest='number', type=int, default=1,
                   help='The number of message you want to produce')
parse.add_argument('--auth-params', dest='auth_params', type=str, default="",
                   help='The auth params which you need to configure the client')
args = parse.parse_args()

# yyyy-mm-dd hh:mm:ss
currenttime= strftime("%Y-%m-%d %H:%M:%S",gmtime())

host = os.uname()[1]

def do_nothing(obj):
    pass

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def IP_address():
        try:
            s = socket.socket(socket_family, socket.SOCK_DGRAM)
            s.connect(external_IP_and_port)
            answer = s.getsockname()
            s.close()
            return answer[0] if answer else None
        except socket.error:
            return None

# Get MAC address of a local interfaces
def psutil_iface(iface):
    # type: (str) -> Optional[str]
    import psutil
    nics = psutil.net_if_addrs()
    if iface in nics:
        nic = nics[iface]
        for i in nic:
            if i.family == psutil.AF_LINK:
                return i.address

# - start timing
starttime = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
start = time.time()

external_IP_and_port = ('198.41.0.4', 53)  # a.root-servers.net
socket_family = socket.AF_INET

# Set up OLED
oled = sh1106(i2c(port=1, address=0x3C), rotate=2, height=128, width=128)
oled.cleanup = do_nothing

# Set Constants
MAX_DISTANCE_MM = 800 # Distance at which our bar is full
TRIGGER_DISTANCE_MM = 80

# Ip address
host_name = socket.gethostname()
ipaddress = IP_address() 

# bh1745
bh1745 = BH1745()
bh1745.setup()
bh1745.set_leds(1)
r, g, b, c = bh1745.get_rgbc_raw()
bh1745.set_leds(0)

# VL53L1X
tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)

# ltr559
ltr559 = LTR559()

# lsm303d
lsm = LSM303D(0x1d)

print(args.service_url)
print(args.auth_params)
# pulsar
# client = pulsar.Client('pulsar://pulsar1:6650') # Local
client = pulsar.Client(args.service_url, authentication=AuthenticationOauth2(args.auth_params))

#sensorschema = AvroSchema(breakoutsensor)
#print("Schema info is: " + sensorschema.schema_info().schema())

#producer = client.create_producer(topic='persistent://public/default/pi-sensors-avro' ,schema=sensorschema,properties={"producer-name": "sensoravro-py-sensor","producer-id": "sensor-avro-sensor" })
producer = client.create_producer(topic=args.topic ,schema=JsonSchema(breakoutsensor),properties={"producer-name": "sensor-py-sensor","producer-id": "sensor-sensor" })
# persistent://public/default/pi-sensors

# loop forever
try:
  while True:
    tof.open() # Initialise the i2c bus and configure the sensor
    tof.start_ranging(2) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
    tof.stop_ranging() # Stop ranging
    distance_in_mm = tof.get_distance() # Grab the range in mm
    distance_in_mm = min(MAX_DISTANCE_MM, distance_in_mm) # Cap at our MAX_DISTANCE

    ltr559.update_sensor()
    lux = ltr559.get_lux()
    prox = ltr559.get_proximity()

    lsm3accl = lsm.accelerometer()
    lsm3mag = lsm.magnetometer()

    # bme680
    try:
        sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    except IOError:
        sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)
    bh1745.set_leds(1)
    r, g, b, c = bh1745.get_rgbc_raw()
    bh1745.set_leds(0)
    uuid2 = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S",gmtime()),uuid.uuid4())
    uniqueid = 'snr_{0}'.format(strftime("%Y%m%d%H%M%S",gmtime()))
    cpuTemp= int(float(getCPUtemperature()))
    cputempf = int(round(9.0/5.0 * float(cpuTemp) + 32))
    usage = psutil.disk_usage("/")

    end = time.time()

    sensorRec = breakoutsensor()
    sensorRec.uuid = uniqueid
    sensorRec.ipaddress = ipaddress
    sensorRec.cputempf = int(cputempf)
    sensorRec.runtime =  int(round(end - start)) 
    sensorRec.host = os.uname()[1]
    sensorRec.hostname = host_name
    sensorRec.macaddress = psutil_iface('wlan0')
    sensorRec.endtime = '{0}'.format( str(end ))
    sensorRec.te = '{0}'.format(str(end-start))
    sensorRec.cpu = float(psutil.cpu_percent(interval=1))
    sensorRec.diskusage = "{:.1f} MB".format(float(usage.free) / 1024 / 1024)
    sensorRec.memory = float(psutil.virtual_memory().percent)
    sensorRec.rowid = str(uuid2)
    sensorRec.systemtime = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
    sensorRec.ts =  int( time.time() )
    sensorRec.starttime = str(starttime)

    sensorRec.BH1745_red = float('{:3.1f}'.format(r))
    sensorRec.BH1745_green = float('{:3.1f}'.format(g))
    sensorRec.BH1745_blue = float('{:3.1f}'.format(b))
    sensorRec.BH1745_clear = float('{:3.1f}'.format(c))
    sensorRec.VL53L1X_distance_in_mm = float(distance_in_mm)
    sensorRec.ltr559_lux = float('{:06.2f}'.format(lux))
    sensorRec.ltr559_prox = float('{:04d}'.format(prox))
    sensorRec.bme680_tempc = float('{0:.2f}'.format(sensor.data.temperature))
    sensorRec.bme680_tempf = float('{0:.2f}'.format((sensor.data.temperature * 1.8) + 32))
    sensorRec.bme680_pressure = float('{0:.2f}'.format(sensor.data.pressure))
    sensorRec.bme680_humidity = float('{0:.3f}'.format(sensor.data.humidity))
    sensorRec.lsm303d_accelerometer = "{:+06.2f}g : {:+06.2f}g : {:+06.2f}g".format(*lsm3accl)
    sensorRec.lsm303d_magnetometer = "{:+06.2f} : {:+06.2f} : {:+06.2f}".format(*lsm3mag)

    print(sensorRec)
    producer.send(sensorRec,partition_key=uniqueid)

    with canvas(oled) as draw:
           draw.rectangle(oled.bounding_box, outline="white", fill="black")
           draw.text((0, 0), "- Apache Pulsar -", fill="white")
           draw.text((0, 10), ipaddress, fill="white")
           draw.text((0, 20), starttime, fill="white")
           draw.text((0, 30), 'Temp: {}'.format( sensor.data.temperature ), fill="white")
           draw.text((0, 40), 'Humidity: {}'.format( sensor.data.humidity ), fill="white")
           draw.text((0, 50), 'Pressure: {}'.format( sensor.data.pressure ), fill="white")
           draw.text((0, 60), 'Distance: {}'.format(str(distance_in_mm)), fill="white")
           draw.text((0, 70), 'CPUTemp: {}'.format( cpuTemp ), fill="white")
           draw.text((0, 80), 'TempF: {}'.format( sensorRec.bme680_tempf ), fill="white")
           draw.text((0, 90), 'A: {}'.format(sensorRec.lsm303d_accelerometer), fill="white")
           draw.text((0, 100), 'M: {}'.format(sensorRec.lsm303d_magnetometer), fill="white")
           draw.text((0, 110), 'DU: {}'.format(sensorRec.diskusage), fill="white")
           time.sleep(0.5)

except KeyboardInterrupt:
  pass

client.close()
