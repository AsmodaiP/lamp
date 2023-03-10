"""Tests for lamp.py."""
from constants import DEFAULT_COLOR
from models import Lamp


def test_turn_on():
    """Test turn on. Turn on lamp twice and check that it is on."""
    lamp = Lamp(DEFAULT_COLOR)
    lamp.turn_on()
    assert lamp.is_on
    lamp.turn_on()
    assert lamp.is_on


def test_turn_off():
    """Test turn off. Turn off lamp twice and check that it is off."""
    lamp = Lamp(DEFAULT_COLOR)
    lamp.turn_on()
    lamp.turn_off()
    assert not lamp.is_on
    lamp.turn_off()
    assert not lamp.is_on


def test_set_color():
    """Test set color. Set color and check that it is set."""
    lamp = Lamp(DEFAULT_COLOR)
    lamp.set_color(16711680)
    assert lamp.color == 16711680
    lamp.set_color(65280)
    assert lamp.color == 65280


def test_handle_command():
    """Test handle command."""
    lamp = Lamp(DEFAULT_COLOR)
    lamp.handle_command('ON')
    assert lamp.is_on
    lamp.handle_command('OFF')
    assert not lamp.is_on
    lamp.handle_command('COLOR', 16711680)
    assert lamp.color == 16711680


def test_unsupported_command():
    """Test unsupported command."""
    lamp = Lamp(DEFAULT_COLOR)
    lamp.handle_command('UNSUPPORTED_COMMAND')
    assert not lamp.is_on
    assert lamp.color == DEFAULT_COLOR
