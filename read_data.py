import re
from typing import NamedTuple
from influxdb import InfluxDBClient
import serial
import chardet
import struct
from time import sleep

INFLUXDB_ADDRESS = '192.168.68.56' #라즈베리파이 아이피
INFLUXDB_USER = 'mqtt'             #INFLUXDB 계정 유저설정
INFLUXDB_PASSWORD = 'mqtt'         #INFLUXDB 계정 비밀번호
INFLUXDB_DATABASE = 'crc_stations'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

class SensorData(NamedTuple):
    location: str
    measurement: str
    value: float

def _parse_mqtt_message(topic, payload):
    match = re.match(topic)
    if match:
        location = match.group(1)
        measurement = match.group(2)
        if measurement == 'status':
            return None
        return SensorData(location, measurement, float(payload))
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

def on_message(datalist):
    #"""The callback for when a PUBLISH message is received from the server."""
    #print(msg.topic + ' ' + str(msg.payload))
    sensor_data = _parse_mqtt_message(datalist[0], datalist)
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)


def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

ser = serial.Serial ("/dev/ttyUSB0", 921600)    #Open port with baud rate
_init_influxdb_database()
while True:
    data = ser.readline()
    received_data = data.decode("ISO-8859-1").encode("utf-8")
    data_list = received_data.split(",")
    on_message(data_list)
