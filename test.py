import serial
import chardet
import struct
import re
from typing import NamedTuple
from influxdb import InfluxDBClient
from time import sleep
import numpy as np

INFLUXDB_ADDRESS = '192.9.65.38' #라즈베리파이 아이피
INFLUXDB_USER = 'dohlee'             #INFLUXDB 계정 유저설정
INFLUXDB_PASSWORD = 'dohlee'         #INFLUXDB 계정 비밀번호
INFLUXDB_DATABASE = 'crc_stations'
BYTE_REGEX = 'sensor/([^/]+)/([^/]+)'
ser = serial.Serial ("/dev/ttyUSB0", 921600)    #Open port with baud rate
influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)



class SensorData(NamedTuple):
    location: str
    measurement: str
    value: float

def _parse_message(topic, data):
    if data == '100-1':
        return None
    match = re.match(BYTE_REGEX, topic)
    if match:
        location = match.group(1)
        measurement = match.group(2)
        if measurement == 'status':
            return None
        return SensorData(location, measurement, float(data))
    else:
        return None

def _send_sensor_data_to_influxdb(sensor_data):
    json_body = [
        {
           'measurement': sensor_data.measurement,
            'tags': {
                'location': sensor_data.location
            },
            'fields': {
               'value': sensor_data.value
           }
        }
    ]
    influxdb_client.write_points(json_body)

def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

_init_influxdb_database()
while True:

    data = ser.readline()

    received_data = data.decode("ISO-8859-1") #.encode("utf-8")
    received_data = received_data + ','
    data_list = received_data.split(',')  #received_data.split(b',')

    sensor_data = _parse_message("sensor/lab/gyrox", data_list[1])
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
    sensor_data = _parse_message("sensor/lab/gyroy", data_list[2])
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
    sensor_data = _parse_message("sensor/lab/gyroz", data_list[3])
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
    sensor_data = _parse_message("sensor/lab/accx", data_list[4])
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
    sensor_data = _parse_message("sensor/lab/accy", data_list[5])
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
    sensor_data = _parse_message("sensor/lab/accz", data_list[6])
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
