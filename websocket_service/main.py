import asyncio

import websockets


async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())

connected_clients = set()


async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        # Here you can also listen for incoming messages from clients if needed
        async for message in websocket:
            # Process incoming messages
            pass
    except:
        connected_clients.remove(websocket)


async def send_updates(message):
    for client in connected_clients:
        await client.send(message)

# This function can be called by your microservice handler when there's an update
