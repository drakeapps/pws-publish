import asyncio
from asyncio_mqtt import Client, MqttError

class MQTT:
	def __init__(self, host, prefix='weather', verbose=False):
		self.prefix = prefix
		self.host = host
		self.client = Client(self.host)
		self.verbose = verbose

	async def connect(self):
		if self.verbose:
			print(f"connecting to mqtt broker {self.host}")
		await self.client.connect()
	
	async def publish(self, data):
		tasks = set()
		for key, value in data.items():
			topic = f"{self.prefix}/{key}"
			message = str(value)
			task = asyncio.create_task(self.post(topic, message))
			tasks.add(task)
		await asyncio.gather(*tasks)
	
	async def post(self, topic, message):
		if self.verbose:
			print(f"mqtt publish: {topic} :: {message}")
		await self.client.publish(topic,message)
