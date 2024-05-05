from typing import Tuple, List, Any
import aiohttp
from pydantic import BaseModel
from trader.env import Env
from trader.lib.parallel_execute import parallel_execute


class FuturePriceModel(BaseModel):
    symbol: str
    priceChange: float
    priceChangePercent: float
    weightedAvgPrice: float
    lastPrice: float
    lastQty: float
    openPrice: float
    highPrice: float
    lowPrice: float
    volume: float
    quoteVolume: float
    openTime: float
    closeTime: float
    firstId: int
    lastId: int
    count: int


class FuturePrice:
    settings: Env

    def __init__(self, settings: Env) -> None:
        self.settings = settings

    async def _do_request(self, url: str, session: aiohttp.ClientSession):
        async with session.get(url) as response:
            return response.status, await response.json()

    async def get_price(self, symbol: str) -> Tuple[int, FuturePriceModel]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.settings.FUTURE_URL + "/fapi/v1/ticker/24hr" + f"?symbol={symbol}"
            ) as response:
                return response.status, FuturePriceModel.model_validate(
                    await response.json()
                )

    async def get_prices(
        self, symbols: List[str]
    ) -> Tuple[int, List[FuturePriceModel | Any]]:
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._do_request(
                    self.settings.FUTURE_URL
                    + "/fapi/v1/ticker/24hr"
                    + f"?symbol={symbol}",
                    session,
                )
                for symbol in symbols
            ]
            results = await parallel_execute(tasks)
            data_list: List[FuturePriceModel] = []
            for res in results:
                if res[0] == 200:
                    data_list.append(FuturePriceModel.model_validate(res[1]))
                    continue
                return res
            return 200, data_list
