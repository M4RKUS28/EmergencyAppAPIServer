import time
from datetime import datetime

import requests
import json
import socket
import os

from SQLLiteDB import SQLiteDB


class FirehoseListener:

    def __init__(self):
        # work around to get IP address on hosts with non resolvable hostnames
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.IP_ADRRESS = s.getsockname()[0]
        s.close()
        self.url = 'http://' + str(self.IP_ADRRESS) + '/update/'
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
                self.apiKey = self.get_API_Key_and_auth()
        except:
            self.apiKey = self.get_API_Key_and_auth()

    def get_API_Key_and_auth(self):
        print("-- No API Key Found --")
        token = input('Enter provided API key here: ')
        f = open("API_KEY.txt", "a")
        f.write(token)
        f.close()
        return token

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
                            #print(event_type, datetime.now())
                            key = event['deviceLocationUpdate']['ipv4']
                            if key:
                                # print("Key: ", key)
                                sqlliteDB = SQLiteDB("./firehoseDB.sqlite")
                                old = sqlliteDB.get(key)
                                count = sqlliteDB.put(key, decoded_line)
                                #if old:
                                    #print(datetime.now(), " - Updated ",
                                    #      json.loads(old)['deviceLocationUpdate']['ipv4'], " to: ", key, " count: ", count)
                                #else:
                                #print(datetime.now(), " - New     ", key, " count: ", count)
                            #else:
                            #    print("INVALID KEY: ", decoded_line)
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
