#!/usr/bin/env python3
from websocket import create_connection
import time,random, asyncio
URL="ws://localhost:8000/"

ws = create_connection("ws://localhost:8000/", keepalive=True)
while True:
    ws.send("bola|{n}".format(n=round(9*random.random())))
    print("Sent")
    print("Receiving...")
    result =  ws.recv()
    print("Received '%s'" % result)
    time.sleep(10)

ws.close()