import os
from trader.env import get_env

env_file_data = """
MONGO_HOST=mongo
MONGO_PORT=27017
MONGO_USERNAME=root
MONGO_PASSWORD=example
FUTURE_URL=https://fapi.binance.com
FUTURE_SECRET=testing
FUTURE_API_KEY=test_api_key
"""


def test_get_env():
    test_env_file_path = "/tmp/testing.env"
    with open(test_env_file_path, "w", encoding="utf-8") as file:
        file.write(env_file_data)
    try:
        env = get_env(test_env_file_path)
        assert env.FUTURE_URL == "https://fapi.binance.com"
        assert env.FUTURE_SECRET == "testing"
        assert env.FUTURE_API_KEY == "test_api_key"
    finally:
        if os.path.exists(test_env_file_path):
            os.remove(test_env_file_path)
