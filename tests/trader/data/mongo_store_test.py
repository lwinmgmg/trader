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

@pytest.mark.asyncio
async def test_mongo_store_insert_one():
    # Arrange
    db_name = "test_db"
    col_name = "test_col"
    data = {"foo":"bar"}
    store = MockMongoStore(db_name=db_name, col_name=col_name)

    # Act for client
    async with store as store:
        res = await store.insert_one(data)
        # Assert
        assert res.inserted_id
        async with store.collection as collection:
            result = await collection.find_one({"_id": res.inserted_id})
            assert result["foo"] == data["foo"]

@pytest.mark.asyncio
async def test_mongo_store_insert_many():
    # Arrange
    db_name = "test_db"
    col_name = "test_col"
    data_list = [{"foo":"bar"}, {"foo":"abc"}]
    store = MockMongoStore(db_name=db_name, col_name=col_name)

    # Act for client
    async with store as store:
        res = await store.insert_many(data_list)
        # Assert
        assert res.inserted_ids
        async with store.collection as collection:
            for data in data_list:
                result = await collection.find_one({"_id": data["_id"]})
                assert result["foo"] == data["foo"]

@pytest.mark.asyncio
async def test_mongo_store_find_one():
    # Arrange
    db_name = "test_db"
    col_name = "test_col"
    data = {"foo":"bar"}
    store = MockMongoStore(db_name=db_name, col_name=col_name)

    # Act for client
    async with store as store:
        async with store.collection as collection:
            res = await collection.insert_one(data)
            result = await store.find_one({"_id": res.inserted_id})
            # Assert
            assert res.inserted_id
            assert result["foo"] == data["foo"]

@pytest.mark.asyncio
async def test_mongo_store_find():
    # Arrange
    db_name = "test_db"
    col_name = "test_col"
    data_list = [{"foo":"bar"}, {"foo":"abc"}]
    store = MockMongoStore(db_name=db_name, col_name=col_name)

    # Act for client
    async with store as store:
        async with store.collection as collection:
            res = await collection.insert_many(data_list)
            results = store.find({"_id": {"$in": res.inserted_ids}})
            # Assert
            
            async for result in results:
                assert result["foo"] == data_list[0]["foo"] or result["foo"] == data_list[1]["foo"]
