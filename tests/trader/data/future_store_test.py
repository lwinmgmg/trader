from unittest.mock import patch
import pytest
from bson import ObjectId
from tests.mocks.aiohttp_mock import FakeClientSession
from trader.data.symbol_enums import Symbol
from trader.data.future_store import FutureStore


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_update_price(mock_get):
    # Arrange
    mock_get.return_value = FakeClientSession()
    db_name = "test_db"
    col_name = "test_col"
    future_store = FutureStore(Symbol.BTC.value, db_name, col_name)

    # Act
    res = await future_store.update_prices()
    print(res.id)
    inserted_result = await future_store.find_one({"_id": ObjectId(res.id)})
    print(inserted_result)
    # Assert
    assert res.id
    assert res.time == inserted_result["time"]
    async with future_store.client as client:
        client.drop_database(db_name)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_update_price_failed(mock_get):
    # Arrange
    mock_get.return_value = FakeClientSession()
    db_name = "test_db"
    col_name = "test_col"
    future_store = FutureStore("BTC1USDT", db_name, col_name)

    # Act
    res = await future_store.update_prices()
    # Assert
    assert res is None
    async with future_store.client as client:
        client.drop_database(db_name)
