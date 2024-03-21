import json
from SQLLiteDB import SQLiteDB


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
        value = json.loads(message)
        if value:
            if value['TYPE'] == 'EMERGENCY':
                ip = value['IP']
                if not ip:
                    return
                print(f"Received message from client: ", ip)

                # Send the message back to the client
                # await self.websocket.send("Message received: " + message)
                db = SQLiteDB("EmergencyAppAPIServer.db")
                data = db.get(ip)
                if not data:
                    data = "NONE"
                broad_msg = '{"id": 0, "FLOOR": "Floor 1", "ROOM": "room1", "TYPE": "ALTERT"}'

                # Broadcast the message to all connected clients
                await self.server.broadcast(broad_msg)
            elif value['TYPE'] == 'REQUEST':
                return


