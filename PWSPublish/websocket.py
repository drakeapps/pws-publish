import asyncio
import json
import websockets

class Server:
	def __init__(self, host="localhost", port=6789, verbose=False):
		self._data = {}
		self.CONNS = set()

		self.host = host
		self.port = port

		self.verbose = verbose
	
	async def start_server(self):
		if self.verbose:
			print(f"starting websocket server {self.host}:{self.port}")
		await websockets.serve(self.change_status, self.host, self.port)


	@property
	def data(self):
		return self._data

	@property
	def data_json(self):
		return json.dumps(self.data)

	# i don't think @data.setter works with async, or i was just doing something wrong
	async def set_data(self, data):
		self._data = data
		await self.notify_connections()

	async def notify_connections(self):
		if self.verbose:
			print(f"websocket: notifying connected clients of data change")
		if self.CONNS:
			message = self.data_json
			if self.verbose:
				print(f"websocket: publishing {self.data_json}")
			await asyncio.wait([conn.send(message) for conn in self.CONNS])
	
	async def register(self, websocket):
		self.CONNS.add(websocket)
	
	async def unregister(self, websocket):
		self.CONNS.remove(websocket)
	
	async def change_status(self, websocket, path):
		if self.verbose:
			print(f"websocket: new connection")
		await self.register(websocket)
		try:
			await websocket.send(self.data_json)
			async for message in websocket:
				# get a message, return the full status
				await websocket.send(self.data_json)
		finally:
			await self.unregister(websocket)
