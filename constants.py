"""Constants for the application."""

from enum import Enum

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 9999
DEFAULT_COLOR = 16776960
INVALID_PORT_MESSAGE = 'Invalid port. Port must be in range 1-65535.'


class Commands(str, Enum):
    """Commands for the lamp."""

    ON = 'ON'
    OFF = 'OFF'
    SET_COLOR = 'SET_COLOR'
