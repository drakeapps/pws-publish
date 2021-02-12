import asyncio
from aioinflux import InfluxDBClient

class Influx:
	def __init__(self, db="weather", host="localhost", port=8086, measurement='weather', verbose=False):
		self.db = db
		self.measurement = measurement
		self.client = InfluxDBClient(db=db, host=host, port=port)

		self.verbose = verbose
	
	async def connect(self):
		if self.verbose:
			print(f"influx: creating session")
		await self.client.create_session()
		if self.verbose:
			print(f"influx: creating/selecting database")
		await self.client.create_database(db=self.db)
	
	async def write(self, data):
		point = {
			'measurement': self.measurement,
			'fields': data
		}
		if self.verbose:
			print(f"influx: writing point: {point}")
		await self.client.write(point)

