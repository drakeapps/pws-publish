# Wunderground/Ambient Weather PWS Publisher

Poll Wunderground API or connect to Ambient Weather socket stream to receive current weather station information and publish it to a Websocket server, MQTT broker, and/or InfluxDB.

Your Wunderground API key is found under [member settings](https://www.wunderground.com/member/api-keys).

Create an API key and Application Key under your [Ambient Weather account](https://ambientweather.net/account)

You will need to have either `--wunderground`, `--ambient-weather`, `--ambient-proxy` as arguments, or it won't connect to anything.

## Ambient Proxy

[ambient-proxy](https://github.com/drakeapps/ambient-proxy) is a simple node websocket server that's just replaying the data received from the Ambient Weather Realtime API. I have continuously had issues with the Ambient Weather socket-io API, but have had zero issues with the node one. 

This is a way to use the Node library but maintain all the 

There is a docker-compose target, `publish-ambient-proxy`, that will pull and run the proxy. This uses the same environment variables as the normal Ambient Weather container. 

## Command Line Arguments

```
python main.py -h                                                    
usage: main.py [-h] [--wunderground] [--api-key API_KEY]
               [--station-id STATION_ID] [--ambient-weather]
               [--ambient-api-key AMBIENT_API_KEY]
               [--application-key APPLICATION_KEY] [--ambient-proxy]
               [--ambient-proxy-host AMBIENT_PROXY_HOST]
               [--ambient-proxy-port AMBIENT_PROXY_PORT]
               [--ambient-proxy-method AMBIENT_PROXY_METHOD] [--influx]
               [--influx-host INFLUX_HOST] [--influx-port INFLUX_PORT]
               [--influx-db INFLUX_DB]
               [--influx-measurement INFLUX_MEASUREMENT] [--websocket]
               [--websocket-host WEBSOCKET_HOST]
               [--websocket-port WEBSOCKET_PORT] [--mqtt]
               [--mqtt-broker MQTT_BROKER] [--mqtt-prefix MQTT_PREFIX]
               [--refresh-rate REFRESH_RATE] [--units UNITS] [--verbose]
               [--stdout] [--raw-stdout]

Wunderground/Ambient Weather PWS Publisher

optional arguments:
  -h, --help            show this help message and exit
  --wunderground        enable wunderground api polling
  --api-key API_KEY     wunderground weather api key
  --station-id STATION_ID
                        wunderground station id
  --ambient-weather     enable ambient weather api stream
  --ambient-api-key AMBIENT_API_KEY
                        ambient weather api key
  --application-key APPLICATION_KEY
                        ambient weather application key
  --ambient-proxy       enable ambient weather api stream using a separate
                        ambient websocket proxy
  --ambient-proxy-host AMBIENT_PROXY_HOST
                        ambient weather proxy host
  --ambient-proxy-port AMBIENT_PROXY_PORT
                        ambient weather proxy port
  --ambient-proxy-method AMBIENT_PROXY_METHOD
                        ambient weather proxy method (ws or wss)
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
# wunderground example
python3 main.py --api-key 1234567890abcdef --station-id KTXHOUST3324 --wunderground --influx --websocket --mqtt
```
