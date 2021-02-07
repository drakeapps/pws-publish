import asyncio
import socketio

class Stream:
	"""
		I cannot get this to work. I'm, not sure if there's an issue with their API or what. 
		
		The aioambient library silently fails

		This tells me the OPEN is wrong. Going there I get an HTML page
	"""
	def __init__(self, api_key, application_key, device=None, verbose=False):
		self.api_key = api_key
		self.application_key = application_key

		# this might be used to filter out data
		self.device = device

		self.verbose = verbose

		self.sio = socketio.AsyncClient()

		self.sio.on("subscribed", self.handle_message)

		self.sio.on("data", self.handle_message)

	async def handle_message(self, message):
		if self.verbose:
			print(f"ambient new message: {message}")
		await self.callback(message)

	async def run_loop(self, callback):

		self.callback = callback

		url = f"ws://rt.ambientweather.net/?api=1&applicationKey={self.application_key}"
		if self.verbose:
			print(f"ambient: connecting to {url}")
				
		await self.sio.connect(url)

		if self.verbose:
			print(f"ambient: connected, sending init")

		await self.sio.emit('subscribe', {
			'apiKeys': [
				self.api_key
			]
		})

		if self.verbose:
			print(f"ambient: stream initialized")

		await self.sio.wait()
		



















# from aiohttp import ClientSession
# from aioambient import Client


# class Stream:
# 	def __init__(self, api_key, application_key, device=None, verbose=False):
# 		self.api_key = api_key
# 		self.application_key = application_key

# 		self.verbose = verbose

		
	
# 	async def run_loop(self, callback):
# 		self.callback = callback
# 		if self.verbose:
# 			print(f"Connecting to Ambient weather API with API key {self.api_key} Application key {self.application_key}")
		
# 		self.client = Client(self.api_key, self.application_key)
# 		self.client.websocket.async_on_subscribed(self.parse_data)
# 		self.client.websocket.async_on_data(self.parse_data)
# 		self.client.websocket.on_connect(self.connect_message)
# 		self.client.websocket.on_disconnect(self.disconnect_message)

# 		print("starting ambient connection")

# 		await self.client.websocket.connect()

# 		print("ambient connection gone, disconnecting")
		
# 		await self.client.websocket.disconnect()

# 	def connect_message(self):
# 		if self.verbose:
# 			print(f"Connected to Ambient weather API")
	
# 	def disconnect_message(self):
# 		if self.verbose:
# 			print(f"Disconnected from Ambient weather API")
		
# 	async def parse_data(self, data):
# 		print(data)
# 		await self.callback(data)
	