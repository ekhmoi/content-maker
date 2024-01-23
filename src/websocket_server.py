import asyncio
import websockets
import json

class WebSocketServer:
    def __init__(self, host, port, command_switch):
        self.host = host
        self.port = port
        self.command_switch = command_switch 
        self.connected_clients = set()

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

    async def send_message(self, command, data):
        """Send message to all connected clients."""
        message = json.dumps({'command': command, 'data': data})
        tasks = []
        for client in self.connected_clients:
            # Create a task for each message sending coroutine
            task = asyncio.create_task(client.send(message))
            tasks.append(task)

        # Wait for all tasks to complete
        await asyncio.gather(*tasks)

    async def handler(self, websocket, path):
        print('New client connected', websocket)
        self.connected_clients.add(websocket)
        try:
            async for message in websocket:
                # Parse the message and call the respective function
                await self.convert_command(message, websocket)
        finally:
            self.connected_clients.remove(websocket)

    def run(self):
        start_server = websockets.serve(self.handler, self.host, self.port)
        print("Websocket is listening at http://localhost:6789")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

