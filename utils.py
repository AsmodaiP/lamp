"""Utils for app."""
from typing import Optional

from fastapi.websockets import WebSocket
from pydantic import ValidationError

from constants import INVALID_PORT_MESSAGE
from exceptions import InvalidPort
from models import Command


def validate_port(port: int) -> None:
    """Validate port number in range 1-65535."""
    if not 1 <= port <= 65535:
        raise InvalidPort(INVALID_PORT_MESSAGE)


async def parse_command_or_send_error(websocket: WebSocket, data) -> Optional[Command]:
    """Parse command or send error."""
    try:
        command = Command.parse_raw(data)
    except ValidationError:
        await websocket.send_json({'error': 'Invalid command'})
        return None
    return command
