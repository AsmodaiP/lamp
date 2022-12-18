"""Module with Lamp server"""
import asyncio
import logging

import aiohttp

from models import Lamp


class LampServer:
    """Lamp server which create connection."""
    def __init__(self, host: str, port: int, lamp: Lamp):
        self.host = host
        self.port = port

        self.logger = logging.getLogger(__name__)
        self.lamp = lamp

    async def start(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.ws_connect(f"ws://{self.host}:{self.port}/ws") as ws:
                    print("Connected to lamp server")
                    async for msg in ws:
                        print(msg)
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            print(f"Received message: {msg.data}")
            except aiohttp.ClientConnectionError:
                self.logger.error("Connection error")


if __name__ == "__main__":
    lamp_server = LampServer("localhost", 9999, Lamp(123))
    asyncio.run(lamp_server.start())
