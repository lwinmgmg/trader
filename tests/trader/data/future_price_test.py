import pytest
from trader.env import get_env
from trader.data.future_price import FuturePrice


@pytest.mark.asyncio
async def test_future_price():
    settings = get_env()
    future_price = FuturePrice(settings=settings)
    status, data = await future_price.get_price("BTCUSDT")
    assert status == 200
    assert data.symbol == "BTCUSDT"


@pytest.mark.asyncio
async def test_future_prices():
    settings = get_env()
    future_price = FuturePrice(settings=settings)
    symbols = ["BTCUSDT", "ETHUSDT"]
    status, data_list = await future_price.get_prices(symbols)
    assert status == 200
    for data in data_list:
        assert data.symbol in symbols


@pytest.mark.asyncio
async def test_future_prices_failed():
    settings = get_env()
    future_price = FuturePrice(settings=settings)
    symbols = ["BTCUSDT", "ETH1USDT"]
    status, data_list = await future_price.get_prices(symbols)
    assert status != 200
