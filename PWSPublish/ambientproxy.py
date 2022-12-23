import asyncio
import json
import websockets

class Proxy:
	def __init__(self, host="ambient-proxy", port=8080, method="ws", verbose=False):
		self.uri = f"{method}://{host}:{port}"
		self.verbose = verbose
	
	async def run_loop(self, callback):
		if self.verbose:
			print(f"ambient-proxy: connecting to {self.uri}")
		async with websockets.connect(self.uri) as websocket:
			if self.verbose:
				print(f"ambient-proxy: connected to {self.uri}")
			while 1:
				data = await websocket.recv()
				if self.verbose:
					print(f"ambient-proxy: received data - {data}")
				callback(json.loads(data))