"""Main Function
"""

# pylint: disable=broad-exception-caught
from typing import List
import logging
import asyncio
from trader.env import get_env
from trader.lib.parallel_execute import parallel_execute
from trader.data.future_store import FutureStore

_logger = logging.getLogger(__name__)
settings = get_env()


async def future_price_update_background(*stores: List[FutureStore]):
    """Function for all price update"""
    try:
        await parallel_execute([store.update_prices() for store in stores])
    except Exception as err:
        _logger.error("Error on updating price %s", err)


async def background(eth_fprice: FutureStore):
    """Background Non Blocking Thread"""
    while True:
        await parallel_execute([future_price_update_background(eth_fprice)])
        await asyncio.sleep(1)


async def async_main():
    """Async Main"""
    eth_fprice = FutureStore("ETHUSDT", db_name="db", col_name="eth_fprice")
    asyncio.create_task(background(eth_fprice))
    while True:
        if eth_fprice.store:
            print(eth_fprice.store[-1])
        await asyncio.sleep(5)


def main():
    """Program Starter"""
    asyncio.run(async_main())
