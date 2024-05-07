from motor import MotorClient
from trader.services.mongo_conn import (
    get_motor_client,
    get_mongo_client_mgr,
    MongoContextManager,
    MongoDbContextManager,
    MongoColContextManager,
)


class MongoStore:
    def __init__(self, db_name: str = "db", col_name: str = "future") -> None:
        self.db_name = db_name
        self.col_name = col_name

    @property
    def m_client(self) -> MotorClient:
        return get_motor_client()

    @property
    def db(self) -> MongoDbContextManager:
        return MongoDbContextManager(client=self.m_client, db_name=self.db_name)

    @property
    def collection(self) -> MongoColContextManager:
        return MongoColContextManager(
            client=self.m_client, db_name=self.db_name, col_name=self.col_name
        )

    @property
    def client(self) -> MongoContextManager:
        return get_mongo_client_mgr(self.m_client)
