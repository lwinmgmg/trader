import pytest
from trader.services.mongo_conn import get_mongo_client_mgr, get_motor_client


@pytest.mark.asyncio
async def test_get_mongo_client_mgr():
    # Arrange
    data = {"foo": "bar"}
    db_name = "test_db"
    m_client = get_motor_client()
    # Act
    try:
        async with get_mongo_client_mgr(m_client) as client:
            db = client[db_name]
            col = db["test_collection"]
            res = await col.insert_one(data)

            # Assert
            assert res.inserted_id
            result = await col.find_one({"_id": res.inserted_id})
            assert result["foo"] == data["foo"]
    finally:
        m_client = get_motor_client()
        await m_client.drop_database(db_name)
        m_client.close()


@pytest.mark.asyncio
async def test_get_motor_client():
    # Arrange
    data = {"foo": "bar"}
    database_name = "test_db"
    # Act
    client = get_motor_client()
    try:
        db = client[database_name]
        col = db["test_collection"]
        res = await col.insert_one(data)

        # Assert
        assert res.inserted_id
        result = await col.find_one({"_id": res.inserted_id})
        assert result["foo"] == data["foo"]
    finally:
        await client.drop_database(database_name)
        client.close()
