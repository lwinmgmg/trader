from typing import Any, Optional
from unittest.mock import patch
import pytest
from trader.env import get_env
from trader.data.future_price import FuturePrice


class FakeAsyncContextMgr:
    def __init__(self, status: int, data: Any) -> None:
        self.status = status
        self.data = data

    async def json(self):
        return self.data

    async def __aexit__(
        self,
        exc_type: Optional[Any],
        exc: Optional[Any],
        tb: Optional[Any],
    ) -> None: ...

    async def __aenter__(self) -> Any:
        return self


class FakeClientSession:
    async def __aexit__(
        self,
        exc_type: Optional[Any],
        exc: Optional[Any],
        tb: Optional[Any],
    ) -> None: ...

    async def __aenter__(self) -> Any:
        return self

    def get(
        self, url: str, *, allow_redirects: bool = True, **kwargs: Any
    ) -> FakeAsyncContextMgr:
        """Perform HTTP GET request."""
        settings = get_env()
        res_map = {
            settings.FUTURE_URL
            + "/fapi/v1/ticker/24hr"
            + "?symbol=BTCUSDT": {
                "status": 200,
                "data": {
                    "symbol": "BTCUSDT",
                    "priceChange": "-94.99999800",
                    "priceChangePercent": "-95.960",
                    "weightedAvgPrice": "0.29628482",
                    "lastPrice": "4.00000200",
                    "lastQty": "200.00000000",
                    "openPrice": "99.00000000",
                    "highPrice": "100.00000000",
                    "lowPrice": "0.10000000",
                    "volume": "8913.30000000",
                    "quoteVolume": "15.30000000",
                    "openTime": 1499783499040,
                    "closeTime": 1499869899040,
                    "firstId": 28385,
                    "lastId": 28460,
                    "count": 76,
                },
            },
            settings.FUTURE_URL
            + "/fapi/v1/ticker/24hr"
            + "?symbol=BTC1USDT": {"status": 400, "data": {"message": "Failed"}},
            settings.FUTURE_URL
            + "/fapi/v1/ticker/24hr"
            + "?symbol=ETHUSDT": {
                "status": 200,
                "data": {
                    "symbol": "ETHUSDT",
                    "priceChange": "-94.99999800",
                    "priceChangePercent": "-95.960",
                    "weightedAvgPrice": "0.29628482",
                    "lastPrice": "4.00000200",
                    "lastQty": "200.00000000",
                    "openPrice": "99.00000000",
                    "highPrice": "100.00000000",
                    "lowPrice": "0.10000000",
                    "volume": "8913.30000000",
                    "quoteVolume": "15.30000000",
                    "openTime": 1499783499040,
                    "closeTime": 1499869899040,
                    "firstId": 28385,
                    "lastId": 28460,
                    "count": 76,
                },
            },
            settings.FUTURE_URL
            + "/fapi/v1/ticker/24hr"
            + "?symbol=ETH1USDT": {"status": 400, "data": {"message": "Failed"}},
        }
        return FakeAsyncContextMgr(res_map[url].get("status"), res_map[url].get("data"))


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
    assert status != 200


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
    assert status != 200
