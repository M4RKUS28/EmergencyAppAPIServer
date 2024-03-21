

class Server:
    def __init__(self):
        self.clients = set()

    def register(self, websocket, path):
        client = Client(websocket, path)
        client.server = self  # Now the client can access server for broadcasting
        self.clients.add(client)
        return client.handler()

    async def handler(self, websocket, path):
        self.clients.add(await self.register(websocket, path))
