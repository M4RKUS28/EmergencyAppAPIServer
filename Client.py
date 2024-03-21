import json
from SQLLiteDB import SQLiteDB


class Client:
    def __init__(self, websocket, path, server):
        self.server = server
        self.websocket = websocket
        self.path = path

    async def handler(self):
        async for message in self.websocket:
            try:
                await self.handle_message(message)
            except Exception as e:
                print("Error while handling message: ", e)

    async def handle_message(self, message):
        print(" > handle_message: ", message)
        if message == "ping":
            return

        # await self.websocket.send("Message received: " + message)
        value = None
        try:
            value = json.loads(message)
        except json.JSONDecodeError:
            print("Decoding JSON has failed")
            return
        else:
            print("Decoding JSON has succeeded")

        if value['TYPE'] == 'EMERGENCY':
            try:
                ip = value['IP']
            except Exception as e:
                print("Error failed to extract IP")
                return
            print(f"Received message from client: ", ip)

            # Send the message back to the client
            #db = SQLiteDB("EmergencyAppAPIServer.db")
            #data = db.get(ip)
            #if not data:
            #    data = "NONE"
            broad_msg = '{"id": 0, "FLOOR": "Floor 3", "ROOM": "Room B41", "TYPE": "FIRE"}'

            # Broadcast the message to all connected clients
            try:
                await self.server.broadcast(broad_msg, self)
            except Exception as e:
                print("caught exception in broadcast: ", e)

        elif value['TYPE'] == 'REQUEST':
            print("received message from client: ", value[''])

