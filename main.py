import argparse
import asyncio
import json

from PWSPublish import wunderground
from PWSPublish import ambient
from PWSPublish import mqtt
from PWSPublish import websocket
from PWSPublish import influxdb


parser = argparse.ArgumentParser(description='Wunderground/Ambient Weather PWS Publisher')

parser.add_argument('--wunderground', help="enable wunderground api polling", action='store_true')
parser.add_argument('--api-key', help="wunderground weather api key")
parser.add_argument('--station-id',  help="wunderground station id")

parser.add_argument('--ambient-weather', help="enable ambient weather api stream", action='store_true')
parser.add_argument('--ambient-api-key', help="ambient weather api key")
parser.add_argument('--application-key', help="ambient weather application key")

parser.add_argument('--influx', help='publish to influxdb', action='store_true')
parser.add_argument("--influx-host", help="InfluxDB Host", default="localhost")
parser.add_argument("--influx-port", help="InfluxDB Port", type=int, default=8086)
parser.add_argument("--influx-db", help="InfluxDB Database", default="weather")
parser.add_argument("--influx-measurement", help="InfluxDB Name of Measurement for point", default="weather")

parser.add_argument('--websocket', help="publish to WebSocket server", action='store_true')
parser.add_argument('--websocket-host', help='WebSocket server host', default='localhost')
parser.add_argument('--websocket-port', help='WebSocket server port', type=int, default=6789)

parser.add_argument('--mqtt', help='publish to MQTT broker', action='store_true')
parser.add_argument('--mqtt-broker', help='MQTT broker', default='localhost')
parser.add_argument('--mqtt-prefix', help='MQTT prefix for messages. ex: weather -> weather/windSpeed', default='weather')

parser.add_argument('--refresh-rate', help="time between Wunderground API requests", type=int, default=60)
parser.add_argument('--units', help='units for wunderground api to return. e=imperial. m=metric. h=hybrid (uk)', default='e')

parser.add_argument('--verbose', help="Add debug messages", action='store_true')
parser.add_argument('--stdout', help="Write JSON to stdout of parsed data", action='store_true')
parser.add_argument('--raw-stdout', help="Write JSON to stdout of raw API data", action='store_true')


args = parser.parse_args()

if args.wunderground:
	wunderground_api = wunderground.API(args.api_key, args.station_id, units=args.units, verbose=args.verbose)
else:
	wunderground_api = None

if args.ambient_weather:
	ambient_weather_api = ambient.Stream(args.api_key, args.application_key, device=args.station_id, verbose=args.verbose)
else:
	ambient_weather_api = None

if args.mqtt:
	if args.verbose:
		print(f"MQTT enabled")
	mqtt_publish = mqtt.MQTT(host=args.mqtt_broker, prefix=args.mqtt_prefix, verbose=args.verbose)
else:
	mqtt_publish = None

if args.websocket:
	if args.verbose:
		print("WebSocket Server enabled")
	websocket_server = websocket.Server(args.websocket_host, args.websocket_port, verbose=args.verbose)
else:
	websocket_server = None

if args.influx:
	if args.verbose:
		print(f"InfluxDB enabled")
	influx_publish = influxdb.Influx(host=args.influx_host, db=args.influx_db, port=args.influx_port, measurement=args.influx_measurement, verbose=args.verbose)
else:
	influx_publish = None


async def publish_data(data):
	tasks = set()

	if mqtt_publish:
		task = asyncio.create_task(mqtt_publish.publish(data))
		tasks.add(task)
	
	if websocket_server:
		task = asyncio.create_task(websocket_server.set_data(data))
		tasks.add(task)
	
	if influx_publish:
		task = asyncio.create_task(influx_publish.write(data))
		tasks.add(task)

	if args.stdout:
		print(json.dumps(data))

	await asyncio.gather(*tasks)

async def main():
	if mqtt_publish:
		await mqtt_publish.connect()
	if websocket_server:
		await websocket_server.start_server()
	if influx_publish:
		await influx_publish.connect()

	
	# run wunderground and ambient concurrently
	tasks = set()
	if wunderground_api:
		task = asyncio.create_task(wunderground_api.run_loop(publish_data, refresh_rate=args.refresh_rate))
		tasks.add(task)
	
	if ambient_weather_api:
		task = asyncio.create_task(ambient_weather_api.run_loop(publish_data))
		tasks.add(task)
	
	await asyncio.gather(*tasks)
	

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
