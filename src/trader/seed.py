"""Seed Function
"""

import asyncio
from motor import MotorDatabase
from trader.data.table_enums import MongoTable
from trader.services.mongo_conn import get_motor_client


async def feth_indexes(db: MotorDatabase):
    """Create index for future ETH table

    Args:
        db (MotorDatabase): _description_
    """
    col = db[MongoTable.FETH.value]
    await col.create_index({"time": -1})


async def fbtc_indexes(db: MotorDatabase):
    """Create index for future BTC table

    Args:
        db (MotorDatabase): _description_
    """
    col = db[MongoTable.FBTC.value]
    await col.create_index({"time": -1})


async def async_main():
    """Seed main async function"""
    m_client = get_motor_client()
    try:
        db = m_client["db"]
        await feth_indexes(db)
        await fbtc_indexes(db)
    finally:
        m_client.close()


def main():
    """Main function"""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
