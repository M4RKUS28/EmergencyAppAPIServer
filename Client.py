

class Client:
    def __init__(self, websocket, path):
        self.websocket = websocket
        self.path = path

    async def handler(self):
        async for message in self.websocket:
            await self.handle_message(message)

    async def handle_message(self, message):
        print(f"Received message from client: {message}")

        # Send the message back to the client
        await self.websocket.send("Message received: " + message)

        # Broadcast the message to all connected clients
        await self.broadcast(message)

    async def broadcast(self, message):
        for client in self.server.clients:
            if client != self:
                await client.websocket.send(message)
