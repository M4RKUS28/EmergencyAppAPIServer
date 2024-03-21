from Client import Client as Client


class Server:
    def __init__(self):
        self.clients = set()

    def register(self, websocket, path):
        client = Client(websocket, path, self)
        client.server = self  # Now the client can access server for broadcasting
        self.clients.add(client)
        return client.handler()

    async def handler(self, websocket, path):
        try:
            client = await self.register(websocket, path)
            self.clients.add(client)
            print("New Connection: ", client)
        except Exception as e:
            print("caught exception")

    async def broadcast(self, message, this):
        disconnected_clients = [client for client in self.clients
                                if client and client.websocket and not client.websocket.open]
        for client in disconnected_clients:
            self.clients.remove(client)

        for client in self.clients:
            if client is this:
                continue
            try:
                await client.websocket.send(message)
            except Exception as e:
                print("Caught Exception: ")