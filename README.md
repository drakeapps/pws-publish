# Wunderground PWS Publisher

Poll Wunderground API to pull current weather station information and publish it to a Websocket server, MQTT broker, and/or InfluxDB.

Your Wunderground API key is found under [member settings](https://www.wunderground.com/member/api-keys).

## Command Line Arguments

```
python main.py -h
usage: main.py [-h] --api-key API_KEY --station-id STATION_ID [--influx]
               [--influx-host INFLUX_HOST] [--influx-port INFLUX_PORT]
               [--influx-db INFLUX_DB]
               [--influx-measurement INFLUX_MEASUREMENT] [--websocket]
               [--websocket-host WEBSOCKET_HOST]
               [--websocket-port WEBSOCKET_PORT] [--mqtt]
               [--mqtt-broker MQTT_BROKER] [--mqtt-prefix MQTT_PREFIX]
               [--refresh-rate REFRESH_RATE] [--units UNITS] [--verbose]
               [--stdout] [--raw-stdout]

Wunderground PWS Publisher

optional arguments:
  -h, --help            show this help message and exit
  --api-key API_KEY     wunderground api key
  --station-id STATION_ID
                        wunderground station id
  --influx              publish to influxdb
  --influx-host INFLUX_HOST
                        InfluxDB Host
  --influx-port INFLUX_PORT
                        InfluxDB Port
  --influx-db INFLUX_DB
                        InfluxDB Database
  --influx-measurement INFLUX_MEASUREMENT
                        InfluxDB Name of Measurement for point
  --websocket           publish to WebSocket server
  --websocket-host WEBSOCKET_HOST
                        WebSocket server host
  --websocket-port WEBSOCKET_PORT
                        WebSocket server port
  --mqtt                publish to MQTT broker
  --mqtt-broker MQTT_BROKER
                        MQTT broker
  --mqtt-prefix MQTT_PREFIX
                        MQTT prefix for messages. ex: weather ->
                        weather/windSpeed
  --refresh-rate REFRESH_RATE
                        time between Wunderground API requests
  --units UNITS         units for wunderground api to return. e=imperial.
                        m=metric. h=hybrid (uk)
  --verbose             Add debug messages
  --stdout              Write JSON to stdout of parsed data
  --raw-stdout          Write JSON to stdout of raw API data
```

## Docker

1. Edit `.env-sample` and copy/move to `.env`
2. Edit `docker-compose.yml` `command` line to enable/disable/edit any other arguments
3. `docker-compose pull` (or build). Images are hosted on GHCR and are built for ARM and x86 on every master commit.
4. `docker-compose up -d`

## Python (venv)

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py --api-key 1234567890abcdef --station-id KTXHOUST3324 --influx --websocket --mqtt
```
