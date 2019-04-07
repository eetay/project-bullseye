#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import json
import time


async def hello(websocket, path):
    x=100
    y=100
    print("CONNECTION")
    while True:
        x=x+5
        greeting = json.dumps({'offsetTop':y,'offsetLeft':x})
        print(f"> {greeting}")
        await websocket.send(greeting)
        time.sleep(1)
    # name = await websocket.recv()
    # print(f"< {name}")


start_server = websockets.serve(hello, 'localhost', 9999)
print("GO!")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

