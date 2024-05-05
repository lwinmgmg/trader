"""Main Function
"""
import asyncio
from trader.env import get_env

settings = get_env()


async def background():
    """Background Non Blocking Thread"""
    while True:
        await asyncio.sleep(1)


async def async_main():
    """Async Main"""
    asyncio.create_task(background())
    await asyncio.sleep(1000)


def main():
    """Program Starter"""
    asyncio.run(async_main())
