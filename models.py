"""Module contains the models for the application."""

from typing import Callable, Dict

from pydantic import BaseModel

from constants import Commands


class Command(BaseModel):
    """Command for the lamp."""

    command: str
    metadata: float


class Lamp:
    """Lamp model."""

    def __init__(self, color: int, is_on=False):
        self.color = color
        self.is_on = is_on

    def turn_on(self):
        """Turn on the lamp."""
        self.is_on = True

    def turn_off(self):
        """Turn off the lamp."""
        self.is_on = False

    def set_color(self, color: int):
        """Set lamp color to the given int value."""
        self.color = color

    def handle_command(self, command, *args):
        """Handle the given command with the given arguments."""
        command_dict: Dict[str, Callable] = {
            Commands.ON: self.turn_on,
            Commands.OFF: self.turn_off,
            Commands.SET_COLOR: self.set_color
        }
        func = command_dict.get(command)
        if func:
            if func.__code__.co_argcount != 1:
                func(*args)
                return
            func()

    def __dict__(self):
        """Return dict representation of the lamp."""
        return {'color': self.color, 'is_on': self.is_on}
