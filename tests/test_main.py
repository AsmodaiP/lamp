"""Test main.py."""

from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

from constants import DEFAULT_COLOR, Commands
from main import app
from models import Command


def test_invalid_command():
    """Test invalid command."""
    client = TestClient(app)
    with client.websocket_connect('/ws_self') as websocket:
        websocket: WebSocket
        data = websocket.send_json({'msg': 'Hello WebSocket'})
        data = websocket.receive_json()
        assert data == {'error': 'Invalid command'}


def test_turn_on():
    """Test turn on. Turn on lamp twice and check that it is on."""
    command = Command(command=Commands.ON, metadata=0)
    client = TestClient(app)
    with client.websocket_connect('/ws_self') as websocket:
        websocket: WebSocket
        data = websocket.send_json(command.dict())
        data = websocket.receive_json()
        assert data == {'color': DEFAULT_COLOR, 'is_on': True}


def test_turn_off():
    """Test turn off. Turn off lamp twice and check that it is off."""
    command_off = Command(command=Commands.OFF, metadata=0)
    command_on = Command(command=Commands.ON, metadata=0)
    client = TestClient(app)
    with client.websocket_connect('/ws_self') as websocket:
        websocket: WebSocket
        data = websocket.send_json(command_on.dict())
        data = websocket.receive_json()
        assert data['is_on']

        data = websocket.send_json(command_off.dict())
        data = websocket.receive_json()
        assert not data['is_on']


def test_set_color():
    """Test set color. Set color and check that it is set."""
    command = Command(command=Commands.SET_COLOR, metadata=16711680)
    client = TestClient(app)
    with client.websocket_connect('/ws_self') as websocket:
        websocket: WebSocket
        data = websocket.send_json(command.dict())
        data = websocket.receive_json()
        assert data['color'] == 16711680


def test_not_change_color_when_turn():
    """Test not change color when turn on/off."""
    command_off = Command(command=Commands.OFF, metadata=0)
    command_on = Command(command=Commands.ON, metadata=0)
    command_set_color = Command(command=Commands.SET_COLOR, metadata=16711680)
    client = TestClient(app)
    with client.websocket_connect('/ws_self') as websocket:
        websocket: WebSocket

        data = websocket.send_json(command_on.dict())
        data = websocket.receive_json()
        assert data['color'] == DEFAULT_COLOR

        data = websocket.send_json(command_set_color.dict())
        data = websocket.receive_json()
        assert data['color'] == 16711680

        data = websocket.send_json(command_off.dict())
        data = websocket.receive_json()
        assert data['color'] == 16711680

        data = websocket.send_json(command_off.dict())
        data = websocket.receive_json()
        assert data['color'] == 16711680


def test_not_change_state_when_set_color():
    """Test not change state when set color."""
    command_off = Command(command=Commands.OFF, metadata=0)
    command_on = Command(command=Commands.ON, metadata=0)
    command_set_color = Command(command=Commands.SET_COLOR, metadata=16711680)
    client = TestClient(app)
    with client.websocket_connect('/ws_self') as websocket:
        websocket: WebSocket
        data = websocket.send_json(command_on.dict())
        data = websocket.receive_json()
        assert data['is_on']

        data = websocket.send_json(command_set_color.dict())
        data = websocket.receive_json()
        assert data['is_on']

        data = websocket.send_json(command_off.dict())
        data = websocket.receive_json()
        assert not data['is_on']
