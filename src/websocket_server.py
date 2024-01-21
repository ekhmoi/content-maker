import asyncio
import websockets
import json

class WebSocketServer:
    def __init__(self, host, port, command_switch):
        self.host = host
        self.port = port
        self.command_switch = command_switch 

    async def convert_command(self, request_data, websocket):
        data_dict = json.loads(request_data)
        data = data_dict['data']
        command = data_dict['command']
        func = self.command_switch.get(command)

        # If the function exists, call it
        if func:
            result = func(data)
            await websocket.send(json.dumps({ 'command': f'{command}_result', 'data': result }))

        else:
            # Handle unknown command
            print(f"Unknown command: {command}")
            await websocket.send(json.dumps({'command': f'{command}_result', 'error': 'command failed', result: None}))


    async def handler(self, websocket, path):
        async for message in websocket:
            # Parse the message and call the respective function
            await self.convert_command(message, websocket)

    def run(self):
        start_server = websockets.serve(self.handler, self.host, self.port)
        print("Websocket is listening at http://localhost:6789")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
