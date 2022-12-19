"""Main module of the application."""
import argparse
import asyncio
import time

import uvicorn
import websockets
from fastapi import FastAPI, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocket
from pydantic import ValidationError

from constants import DEFAULT_COLOR, DEFAULT_HOST, DEFAULT_PORT
from models import Command, Lamp
from utils import parse_command_or_send_error, validate_port

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    """Index page with the lamp control panel."""
    return templates.TemplateResponse('index.html', {'request': request})


@app.websocket('/ws')
async def websocket_cli_server(websocket: WebSocket):
    """Websocket endpoint for the lamp control."""
    await websocket.accept()
    while True:
        input_data = input()
        import json
        input_as_json = json.loads(input_data)
        await websocket.send_json(input_as_json)
        data = await websocket.receive()
        print(data)


@app.websocket('/ws_self')
async def websocket_endpoint_for_site(websocket: WebSocket):
    """Websocket endpoint for the lamp control."""
    lamp = Lamp(DEFAULT_COLOR)
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            try:
                command = Command.parse_raw(data)
            except ValidationError:
                await websocket.send_json({'error': 'Invalid command'})
                continue
            metadata = command.metadata
            lamp.handle_command(command.command, metadata)
            await websocket.send_json(lamp.__dict__())
        except WebSocketDisconnect:
            break


async def websocket_end(websocket: WebSocket):
    """Websocket endpoint for the lamp control."""
    lamp = Lamp(DEFAULT_COLOR)
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            try:
                command = Command.parse_raw(data)
            except ValidationError:
                await websocket.send_json({'error': 'Invalid command'})
                continue
            metadata = command.metadata
            lamp.handle_command(command.command, metadata)
            await websocket.send_json(lamp.__dict__())
        except WebSocketDisconnect:
            break


def parse_args() -> argparse.Namespace:
    """Parse host and port arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=False,
                        help='server address', default=DEFAULT_HOST, type=str)
    parser.add_argument('--port', required=False,
                        help='server port (1-65535)', default=DEFAULT_PORT, type=int)

    parser.add_argument('--cli_server', required=False, default=False,
                        help='Run server in CLI mode', action='store_true')
    return parser.parse_args()


async def accept_websocket(host, port):
    """Accept websocket connection."""
    lamp = Lamp(DEFAULT_COLOR)
    address = f'ws://{host}:{port}/ws'
    while True:
        try:
            async with websockets.connect(address) as websocket:
                while True:
                    data = await websocket.recv()
                    command = await parse_command_or_send_error(websocket, data)
                    if not command:
                        continue
                    lamp.handle_command(command.command, command.metadata)
                    await websocket.send(str(lamp.__dict__()))
        except websockets.exceptions.ConnectionClosed:
            time.sleep(1)


def start_server() -> None:
    """Start server."""
    args = parse_args()
    host: str = args.host
    port: int = args.port
    validate_port(port)
    if args.cli_server:
        uvicorn.run(app, host=host, port=port)
    asyncio.get_event_loop().run_until_complete(accept_websocket(host, port))
    return None


if __name__ == '__main__':
    event = asyncio.get_event_loop()
    event.run_until_complete(start_server())  # type: ignore
