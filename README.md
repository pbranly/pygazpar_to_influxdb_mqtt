# pygazpar_to_influxdb

![Docker Build Status](https://img.shields.io/docker/cloud/automated/jeoffrey54/pygazpar_to_influxdb.svg) ![Docker Build Status](https://img.shields.io/docker/cloud/build/jeoffrey54/pygazpar_to_influxdb.svg)


This repository uses [PyGazpar](https://github.com/ssenart/PyGazpar) to retrieve natural gas consumption from GrDF French provider, and push it to InfluxDB.
It is designed in order to connect to the version 2.0 of Influx data base

This repository is a fork of the https://github.com/Jeoffreybauvin/pygazpar_to_influxdb dedicated version 1.8 of Influxdb

A tentative configuration is described for Influxdb 1.8 but not tested

## Setup

There is a Docker image ready to use : https://hub.docker.com/repository/docker/pbranly/pygazpar_to_influxdb

Docker compose part is given hereunder:

```bash

#define a pygazpar2 service sans firefox et geckodriver

  pygazpar2:
    container_name: pygazpar2
    image: pbranly/pygazpar_to_influxdb:latest
    env_file:
         - .env
    depends_on:
      - influxdb2
```     

In order to restart regurarly the container, add an entry in the crontab assuming that name of the container is pygazpar2:

type:
crontab -e
then add:
0 */2 * * * docker restart pygazpar2


Parameters to include in your .env file: (please note that all those fields are mandatory. Any field left blank will have as a consequence to crash the program)

For Influxdb 2.0:
With:
- PYGAZPAR_INFLUXDB2_HOST="local ip host of your Influxdb database:port of yourInfluxdb database" exemple: "192.168.1.20:8086"
- PYGAZPAR_INFLUXDB2_TOKEN="token of your Influxdb 2.0 data base (to find in influxdb)"
- PYGAZPAR_INFLUXDB2_BUCKET="name of the influxdb 2 bucket in which you want to write gazpar data"
- PYGAZPAR_INFLUXDB2_ORG="name of your influxdb 2 organization"
- PYGAZPAR_PYGAZPAR_LOGIN="login of your GRDF account"
- PYGAZPAR_PYGAZPAR_PASSWORD="password of your GRDF password"
- PYGAZPAR_PCE_IDENTIFIER="Identifier opf your GRDF PCE (remove blanks)"
- PYGAZPAR_LASTNDAY="number of days of datas " by default put 10

- PYGAZPAR_MQTT_URL="local ip host of your MQTT"
- PYGAZPAR_MQTT_LOGIN="login of your MQTT"
- PYGAZPAR_MQTT_PASSWORD="password of your MQTT"



MQTT_KEEPALIVE_INTERVAL = 3600


For Influxdb 1.8: (not tested)
With:
- PYGAZPAR_INFLUXDB2_HOST="local ip host of your Influxdb database:port of yourInfluxdb database" exemple: "192.168.1.20:8086"
- PYGAZPAR_INFLUXDB2_TOKEN="USERNAME:PASSWORD of your Influxdb 1.8 database)" <------------------
- PYGAZPAR_INFLUXDB2_BUCKET="nDATABASE/RETENTION of your Influxdb 1.8 database. for exemple home_assistant/autogen" <--------------------------
- PYGAZPAR_INFLUXDB2_ORG="_" <-----------------------
- PYGAZPAR_PYGAZPAR_LOGIN="login of your GRDF account"
- PYGAZPAR_PYGAZPAR_PASSWORD="password of your GRDF password"
- PYGAZPAR_PCE_IDENTIFIER="Identifier opf your GRDF PCE (remove blanks)"
- PYGAZPAR_LASTNDAY="number of days of datas " by default put 10

- PYGAZPAR_MQTT_URL="local ip host of your MQTT"
- PYGAZPAR_MQTT_LOGIN="login of your MQTT"
- PYGAZPAR_MQTT_PASSWORD="password of your MQTT"