"""Connection Service For Mongo DB
"""

from motor import MotorClient, MotorCollection, MotorDatabase
from trader.env import get_env

settings = get_env()


class MongoContextManager:
    def __init__(self, client: MotorClient) -> None:
        self.client = client

    async def __aexit__(self, *args, **kwargs):
        self.client.close()

    async def __aenter__(self) -> MotorClient:
        return self.client


class MongoDbContextManager(MongoContextManager):
    def __init__(self, client: MotorClient, db_name: str) -> None:
        self.client = client
        self.db_name = db_name

    async def __aenter__(self) -> MotorDatabase:
        return self.client[self.db_name]


class MongoColContextManager(MongoContextManager):
    def __init__(self, client: MotorClient, db_name: str, col_name: str) -> None:
        self.client = client
        self.db_name = db_name
        self.col_name = col_name

    async def __aenter__(self) -> MotorCollection:
        return self.client[self.db_name][self.col_name]


def get_motor_client() -> MotorClient:
    return MotorClient(
        host=settings.MONGO_HOST,
        port=settings.MONGO_PORT,
        username=settings.MONGO_USERNAME,
        password=settings.MONGO_PASSWORD,
    )


def get_mongo_client_mgr(client: MotorClient) -> MongoContextManager:
    return MongoContextManager(client)
