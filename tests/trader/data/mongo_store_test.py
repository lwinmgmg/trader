import pytest
from trader.data.mongo_store import MongoStore


class MockMongoStore(MongoStore):
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        async with self.client as client:
            client.drop_database(self.db_name)


@pytest.mark.asyncio
async def test_mongo_store_db():
    # Arrange
    db_name = "test_db"
    col_name = "test_col"
    store = MockMongoStore(db_name=db_name, col_name=col_name)

    # Act for db
    async with store as store:
        async with store.db as db:
            col = db[col_name]
            res = await col.insert_one({"foo": "bar"})
            # Assert
            assert res.inserted_id


@pytest.mark.asyncio
async def test_mongo_store_col():
    # Arrange
    db_name = "test_db"
    col_name = "test_col"
    store = MockMongoStore(db_name=db_name, col_name=col_name)

    # Act for db
    async with store as store:
        async with store.collection as col:
            res = await col.insert_one({"foo": "bar"})
            # Assert
            assert res.inserted_id


@pytest.mark.asyncio
async def test_mongo_store_client():
    # Arrange
    db_name = "test_db"
    col_name = "test_col"
    store = MockMongoStore(db_name=db_name, col_name=col_name)

    # Act for client
    async with store as store:
        async with store.client as client:
            db = client[db_name]
            col = db[col_name]
            res = await col.insert_one({"foo": "bar"})
            # Assert
            assert res.inserted_id
