"""Main module of the application."""
import argparse
import asyncio

import uvicorn
from fastapi import FastAPI, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocket
from pydantic import ValidationError

from constants import DEFAULT_COLOR, DEFAULT_HOST, DEFAULT_PORT, INVALID_PORT_MESSAGE
from exceptions import InvalidPort
from models import Command, Lamp

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Index page with the lamp control panel."""
    return templates.TemplateResponse("index.html", {'request': request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
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
    parser.add_argument("--host", required=False,
                        help="server address", default=DEFAULT_HOST, type=str)
    parser.add_argument("--port", required=False,
                        help="server port (1-65535)", default=DEFAULT_PORT, type=int)
    return parser.parse_args()


def validate_port(port: int) -> None:
    """Validate port number in range 1-65535."""
    if not 1 <= port <= 65535:
        raise InvalidPort(INVALID_PORT_MESSAGE)


def start_server() -> None:
    """Start server."""
    args = parse_args()
    host: str = args.host
    port: int = args.port
    validate_port(port)
    uvicorn.run(app, host=host, port=port)
    return None


if __name__ == "__main__":

    event = asyncio.get_event_loop()
    event.run_until_complete(start_server())  # type: ignore
