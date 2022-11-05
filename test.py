import serial
import chardet
import struct
import re
from typing import NamedTuple
from influxdb import InfluxDBClient
from time import sleep

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


while True:
    _init_influxdb_database()
    data = ser.readline()

    received_data = data.decode("ISO-8859-1") #.encode("utf-8")
    data_list = received_data.split(',')  #received_data.split(b',')
    gyro_x =  data_list[1]
    gyro_y = data_list[2]
    gyro_z = data_list[3]
    acc_x = data_list[4]
    acc_y = data_list[5]
    acc_z = data_list[6]
    sensor_battery = data_list[7]
    sensor_channel = data_list[0]
    sensor_data = _parse_message("sensor/lab/gyrox", gyro_x)
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
    sensor_data = _parse_message("sensor/lab/gyroy", gyro_y)
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
    sensor_data = _parse_message("sensor/lab/gyroz", gyro_z)
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
    sensor_data = _parse_message("sensor/lab/accx", acc_x)
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
    sensor_data = _parse_message("sensor/lab/accy", acc_y)
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
    sensor_data = _parse_message("sensor/lab/accz", acc_z)
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
    sensor_data = _parse_message("sensor/lab/battery", sensor_battery)
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
    sensor_data = _parse_message("sensor/lab/channel", sensor_channel)
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
