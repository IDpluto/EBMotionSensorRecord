import serial
import chardet
import struct
import re
from typing import NamedTuple
from influxdb import InfluxDBClient
from time import sleep

INFLUXDB_ADDRESS = '192.168.68.56' #라즈베리파이 아이피
INFLUXDB_USER = 'mqtt'             #INFLUXDB 계정 유저설정
INFLUXDB_PASSWORD = 'mqtt'         #INFLUXDB 계정 비밀번호
INFLUXDB_DATABASE = 'crc_stations'
ser = serial.Serial ("/dev/ttyUSB0", 921600)    #Open port with baud rate

while True:
    data = ser.readline()

    received_data = data.decode("ISO-8859-1").encode("utf-8")
    data_list = received_data.split(",")

    print (data_list[0])
