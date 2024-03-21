import json

class Client:
    def __init__(self, websocket, path, server):
        self.server = server
        self.websocket = websocket
        self.path = path

    async def handler(self):
        async for message in self.websocket:
            await self.handle_message(message)

    async def handle_message(self, message):
        print("handle_message: ", message)

        # await self.websocket.send("Message received: " + message)
        value = json.load(message)
        if value:
            if value['type'] == 'EMERGENCY':
                mac = value['MAC']
                if not mac:
                    return
                print(f"Received message from client: ", mac)

                # Send the message back to the client
                # await self.websocket.send("Message received: " + message)

                broad_msg = json.dumps("")

                # Broadcast the message to all connected clients
                await self.server.broadcast(broad_msg)
            elif value['type'] == 'REQUEST':
                return


