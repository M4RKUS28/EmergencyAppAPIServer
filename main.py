from threading import Thread
import asyncio
import logging
import websockets
from FirehoseListener import FirehoseListener
from Server import Server as Server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    port = 8080
    fireHoseListener = FirehoseListener()
    loop = None

    print("Start DB listener")
    # Start another thread
    thread = Thread(target=fireHoseListener.start_listening)
    thread.start()

    try:
        print("START Server on port", port)
        # Start websockets server

        start_server = websockets.serve(Server().handler, '0.0.0.0', port)

        # Get the main event loop
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    except KeyboardInterrupt:
        # Clean up tasks if an exception is raised (e.g KeyboardInterrupt)
        print(f'Caught keyboard interrupt. Cancelling tasks...')
        fireHoseListener.stop = True
        thread.join()  # make sure the thread finishes
    except Exception as e:
        print('Caught', e)

