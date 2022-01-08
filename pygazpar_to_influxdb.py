#!/usr/bin/env python3

import sys
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from pygazpar.enum import Frequency
import datetime
import argparse
import logging
import re
import decimal
from decimal import Decimal
import pygazpar
import os
import paho.mqtt.client as mqtt
import urllib.parse as urlparse
import ast

url_influxdb = os.environ['PYGAZPAR_INFLUXDB2_HOST']
bucket_influxdb = os.environ['PYGAZPAR_INFLUXDB2_BUCKET']
token_influxdb = os.environ['PYGAZPAR_INFLUXDB2_TOKEN']
org_influxdb = os.environ['PYGAZPAR_INFLUXDB2_ORG']

login_pygazpar = os.environ['PYGAZPAR_PYGAZPAR_LOGIN']
password_pygazpar = os.environ['PYGAZPAR_PYGAZPAR_PASSWORD']
pce_pygazpar = os.environ['PYGAZPAR_PCE_IDENTIFIER']
pce_lastNDays = int(os.environ['PYGAZPAR_LASTNDAY'])

MQTT_HOST = os.environ['PYGAZPAR_MQTT_URL']
MQTT_PORT = 1883
username = os.environ['PYGAZPAR_MQTT_LOGIN']
password = os.environ['PYGAZPAR_MQTT_PASSWORD']
#xxxxxxxxxxxx = os.environ['PYGAZPAR_XXXXXXXXXXXXXXX']
MQTT_TOPIC = "homeassistant/Gazpar"
client_id = "gazpar_gateway"

MQTT_KEEPALIVE_INTERVAL = 3600



parser = argparse.ArgumentParser()

parser.add_argument("--source", help="Source ('json' file must be named data.json. 'pygazpar' asks to pygazpar to retrieve data)", dest="SOURCE", default="pygazpar")

parser.add_argument("-v", "--verbose", dest="verbose_count", action="count", default=0, help="increases log verbosity")

args = parser.parse_args()
log = logging.getLogger()
logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                    format='%(name)s (%(levelname)s): %(message)s')
log.setLevel(max(3 - args.verbose_count, 0) * 10)


influxclient = InfluxDBClient(url=url_influxdb, token=token_influxdb, org=org_influxdb)


write_api = influxclient.write_api(write_options=SYNCHRONOUS)

#------------------------------------------------- 
    
client = pygazpar.Client(username=login_pygazpar, password=password_pygazpar, pceIdentifier=pce_pygazpar, meterReadingFrequency=Frequency.DAILY, lastNDays=pce_lastNDays, tmpDirectory='/tmp')     

log.debug('Starting to update pygazpar data')
client.update()
log.debug('End update pygazpar data')

data = client.data()


jsonInflux = []

for measure in data:
    print(measure)
    date_time_obj = datetime.datetime.strptime(measure['time_period'], '%d/%m/%Y')
    if 'start_index_m3' in measure:
      jsonInflux.append({
        "measurement": "gazpar_consumption_per_day",
        "tags": {
        },
        "time": date_time_obj.strftime('%Y-%m-%dT%H:%M:%S'),
        "fields": {
            "value": measure['volume_m3'],
            "start_index_m3": measure['start_index_m3'],
            "end_index_m3": measure['end_index_m3'],
            "volume_m3": measure['volume_m3'],
            "energy_kwh": measure['energy_kwh'],
            "converter_factor_kwh/m3": measure['converter_factor_kwh/m3'],
            "type": measure['type'],
        }
    })
    else:
      print('No measure')

write_api.write(bucket=bucket_influxdb, record=jsonInflux)


#############################################################################################################################
data = str(client.data()) 

vrai_json = str('{"releves": ' + str(data) + '}').replace("'","\"").replace("u\"","\"");
#print vrai_json
datalist = json.loads(vrai_json);
MQTT_MSG = json.dumps(datalist['releves'][len(datalist['releves'])-1]);
print (datalist)
# Define on_publish event function
def on_publish(client, userdata, mid):
    print("Message Published...");
    sent = 1;

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC);
    client.publish(MQTT_TOPIC, MQTT_MSG);


def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload) # <- do you mean this payload = {...} ?
    payload = json.loads(msg.payload); # you can use json.loads to convert string to json
    print(datalist['releves'][0]);
    print("GRDF data timestamp: " + datalist['releves'][0]['timestamp']); # data retrieval timestamp
    print("Latest available Gazpar data: " + datalist['releves'][len(datalist['releves'])-1]['date']); # latest data available to GRDF
    client.disconnect(); # Got message then disconnect

# Initiate MQTT Client
mqttc = mqtt.Client();

# Register publish callback function
mqttc.on_publish = on_publish;
mqttc.on_connect = on_connect;
mqttc.on_message = on_message;

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL);

# Loop forever
mqttc.loop_forever();