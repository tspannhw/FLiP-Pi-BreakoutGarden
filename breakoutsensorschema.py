import pulsar
import logging
from pulsar.schema import *
from pulsar.schema import AvroSchema
from pulsar.schema import JsonSchema
from pulsar import Client, AuthenticationOauth2

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
