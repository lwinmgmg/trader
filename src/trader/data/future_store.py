from datetime import datetime
from trader.env import get_env
from trader.data.future_price import FuturePrice, FuturePriceModel
from trader.data.mongo_store import MongoStore


class FutureStore(MongoStore):
    def __init__(
        self, symbol: str, db_name: str = "db", col_name: str = "future"
    ) -> None:
        super().__init__(db_name, col_name)
        self.symbol = symbol
        self.settings = get_env()
        self.future_price = FuturePrice(settings=self.settings)

    async def update_prices(self) -> FuturePriceModel | None:
        status, price = await self.future_price.get_price(symbol=self.symbol)
        if status != 200:
            return None
        now_time = int(datetime.utcnow().timestamp())
        price.time = now_time
        res = await self.insert_one(price.model_dump())
        price.id = str(res.inserted_id)
        return price
