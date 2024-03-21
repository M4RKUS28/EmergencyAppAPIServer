import requests
import json
import os

from SQLLiteDB import SQLiteDB


class FirehoseListener:

    def __init__(self):
        self.stop = False

        # Tests to see if we already have an API Key
        try:
            if os.stat("API_KEY.txt").st_size > 0:
                # If we do, lets use it
                f = open("API_KEY.txt")
                self.apiKey = f.read()
                f.close()
            else:
                # If not, lets get user to create one
                print("no api key")
                exit(-1)
        except Exception as e:
            print("no api key ", e)
            exit(-1)

    def start_listening(self):
        while True:
            try:
                s = requests.Session()
                s.headers = {'X-API-Key': self.apiKey}
                r = s.get('https://partners.dnaspaces.io/api/partners/v1/firehose/events', stream=True)
                print("Starting Stream")
                for line in r.iter_lines():
                    if self.stop:
                        break
                    if line:
                        decoded_line = line.decode('utf-8')
                        event = json.loads(decoded_line)
                        event_type = event['eventType']
                        if event_type == 'DEVICE_LOCATION_UPDATE':
                            key = event['deviceLocationUpdate']['ipv4']
                            if key:
                                sqlliteDB = SQLiteDB("./firehoseDB.sqlite")
                                sqlliteDB.put(key, decoded_line)
                                #print("PUT: ", key)
                if self.stop:
                    print("EXIT FirehoseListener")
                    return
                print("-- Restart Stream")
            except KeyboardInterrupt:
                print("Stop FirehoseListener because of KeyboardInterrupt")
                return
            except Exception as e:
                print("Got an exception: ", e)
                continue
