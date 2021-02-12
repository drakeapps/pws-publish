import asyncio
import aiohttp
import json


class API:
	def __init__(self, api_key, station_id, units="e", verbose=False, api_output=False):
		if not api_key or not station_id:
			raise 
		self.api_key = api_key
		self.station_id = station_id
		self.units = units
		self.verbose = verbose
		self.api_output = api_output
	
	async def fetch_current(self):
		if self.verbose:
			print(f"fetching: https://api.weather.com/v2/pws/observations/current?stationId={self.station_id}&format=json&units={self.units}&apiKey={self.api_key}")
		async with aiohttp.ClientSession() as session:
			async with session.get(f"https://api.weather.com/v2/pws/observations/current?stationId={self.station_id}&format=json&units={self.units}&apiKey={self.api_key}") as response:
				resp = await response.text()

				if self.api_output:
					print(resp)
				
				# since this is loading a single station, but the info is put in a object with an array of stations
				# parse it and pull off the excess
				# if we start pulling in multiple weather stations, then we should reconsider this
				parsed = json.loads(resp)
				if len(parsed['observations']) != 1:
					if self.verbose:
						print(f"failed to fetch observation")
					raise
				else:
					if self.verbose:
						print(f"fetched observation")
				return await self.clean_data(parsed['observations'][0])
	
	async def clean_data(self, data):
		"""Clean JSON up, by moving imperial/metric sub object to top level, and add units to as top level key/value"""
		clean = {}
		for key, value in data.items():
			if key in ('imperial', 'metric', 'uk_hybrid'):
				clean['units'] = key
				for k,v in value.items():
					clean[k] = v
			else:
				clean[key] = value
		return clean
	
	async def run_loop(self, callback, refresh_rate=60):
		while 1:
			data = await self.fetch_current()
			await callback(data)
			# this isn't truly an X second refresh rate, since there's a delay in fetching the data and publishing that data
			await asyncio.sleep(refresh_rate)