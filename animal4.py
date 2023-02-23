#!/usr/bin/env python3
import asyncio, redis, websockets, uuid
from redis import StrictRedis

CLIENTS = set()


async def server(websocket, path):
    if websocket.id is None:
        websocket.id = uuid.uuid4()
    CLIENTS.add(websocket)
    while True:
        message = await websocket.recv()
        print(f"Received message: {message} {type(message)}")

        if type(message) == bytes:
            message = message.decode("utf8")
            print(f"Received decoded message: {message}")

        command = message.split("|")
        if len(command) > 1:
            if command[0] == "bola":
                await broadcast(f"bola|{command[1]}")
        await websocket.send("Message received")


async def broadcast(message):
    for websocket in CLIENTS.copy():
        try:
            print("Sending", message, websocket.id)
            await websocket.send(message)
        except websockets.ConnectionClosed:
            print("Connection was lost")
            CLIENTS.remove(websocket)
            pass


async def redis_event_handler(msg):
    print("Handler", msg)
    await broadcast(msg)


redis_server = StrictRedis(host="localhost", port=6379, db=0)
pubsub = redis_server.pubsub()
subscribe_key = "*"
pubsub.psubscribe(**{subscribe_key: redis_event_handler})
pubsub.run_in_thread(sleep_time=0.01)


start_server = websockets.serve(server, "localhost", 8000)

r = redis.Redis()

q = r.pubsub()
q.subscribe("*")


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
