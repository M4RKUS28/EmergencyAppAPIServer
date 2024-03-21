import asyncio
import websockets

import asyncio
import websockets

if __name__ == '__main__':
    port = 80808
    print("START Server on port ", port)
    start_server = websockets.serve(Server().handler, 'localhost', port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
