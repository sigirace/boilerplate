# database/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from configs import get_settings

SET = get_settings().mongo

MONGODB_URL = (
    f"mongodb://{SET.mongodb_id}:{SET.mongodb_pw}"
    f"@{SET.mongodb_host}:{SET.mongodb_port}/?{SET.query_string}"
)


def get_async_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(
        MONGODB_URL,
        connectTimeoutMS=SET.connection_timeout_ms,
        socketTimeoutMS=SET.socket_timeout_ms,
        serverSelectionTimeoutMS=SET.server_selection_timeout_ms,
    )


def get_async_mongo_database(client: AsyncIOMotorClient) -> AsyncIOMotorDatabase:
    return client[SET.mongodb_db]
