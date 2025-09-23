
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from .config import settings

# Async MongoDB client for FastAPI
async_client = None
database = None

# Sync MongoDB client for synchronous operations
sync_client = None
sync_database = None

async def connect_to_mongo():
    """Create database connection"""
    global async_client, database
    async_client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = async_client[settings.DATABASE_NAME]

async def close_mongo_connection():
    """Close database connection"""
    global async_client
    if async_client:
        async_client.close()

def get_sync_database():
    """Get synchronous database connection"""
    global sync_client, sync_database
    if not sync_client:
        sync_client = MongoClient(settings.MONGODB_URL)
        sync_database = sync_client[settings.DATABASE_NAME]
    return sync_database

def get_database():
    """Get async database connection"""
    return database