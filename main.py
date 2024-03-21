import asyncio
import threading

import websockets

from FirehoseListener import FirehoseListener
from Server import Server as Server



if __name__ == '__main__':
    port = 8080
    fireHoseListener = FirehoseListener()
    server = None


    print("START Server on port ", port)
    # Start websockets server
    start_server = websockets.serve(Server().handler, '0.0.0.0', 8765)

    # Get the main event loop
    loop = asyncio.get_event_loop()

    print("Start DB listener")
    # Start another thread
    thread = threading.Thread(target=fireHoseListener.start_listening())
    thread.start()

    try:
        # Start the server
        server = loop.run_until_complete(start_server)

    except KeyboardInterrupt:
        # Clean up tasks if an exception is raised (e.g KeyboardInterrupt)
        print(f'Caught keyboard interrupt. Cancelling tasks...')
        for task in asyncio.all_tasks(loop):
            task.cancel()
        fireHoseListener.stop = True
        thread.join()  # make sure the thread finishes

    except Exception as e:
        print('Caught', e)

    finally:
        server.close()
