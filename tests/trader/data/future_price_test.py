from unittest.mock import patch
import pytest
from trader.env import get_env
from trader.data.future_price import FuturePrice
from tests.mocks.aiohttp_mock import FakeClientSession


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_future_price(mock_get):
    mock_get.return_value = FakeClientSession()
    settings = get_env()
    future_price = FuturePrice(settings=settings)
    status, data = await future_price.get_price("BTCUSDT")
    assert status == 200
    assert data.symbol == "BTCUSDT"


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_future_price_failed(mock_get):
    mock_get.return_value = FakeClientSession()
    settings = get_env()
    future_price = FuturePrice(settings=settings)
    status, _ = await future_price.get_price("BTC1USDT")
    assert status == 400


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_future_prices(mock_get):
    mock_get.return_value = FakeClientSession()
    settings = get_env()
    future_price = FuturePrice(settings=settings)
    symbols = ["BTCUSDT", "ETHUSDT"]
    status, data_list = await future_price.get_prices(symbols)
    print(data_list)
    assert status == 200
    for data in data_list:
        assert data.symbol in symbols


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_future_prices_failed(mock_get):
    mock_get.return_value = FakeClientSession()
    settings = get_env()
    future_price = FuturePrice(settings=settings)
    symbols = ["BTCUSDT", "ETH1USDT"]
    status, data_list = await future_price.get_prices(symbols)
    assert status == 400
