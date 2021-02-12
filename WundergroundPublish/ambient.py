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

		self.sio = socketio.AsyncClient(logger=True, engineio_logger=True)

	async def handle_message(self, message):
		if self.verbose:
			print(f"ambient new message: {message}")
		# right now, we're assuming one device connected
		# TODO: not that
		device_info = message[0]
		await self.callback(device_info)
	
	async def disconnect(self, message):
		if self.verbose:
			print(f"ambient: disconnected")

	async def run_loop(self, callback):

		self.callback = callback

		url = f"https://rt.ambientweather.net/?api=1&applicationKey={self.application_key}"
		if self.verbose:
			print(f"ambient: connecting to {url}")
				
		await self.sio.connect(url)

		if self.verbose:
			print(f"ambient: connected, sending init")
		
		self.sio.on("subscribed", self.handle_message)

		self.sio.on("data", self.handle_message)

		# self.sio.on("disconnect", self.disconnect)

		await self.sio.emit('subscribe', {
			'apiKeys': [
				self.api_key
			]
		})

		if self.verbose:
			print(f"ambient: stream initialized")
		
		await self.sio.wait()
		print(f"ambient: sio wait finished")

