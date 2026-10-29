from pymongo import AsyncMongoClient
from src.models.users import User
from src.config import settings
from beanie import init_beanie


class MongoConnector:
    def __init__(self):
        self.client: AsyncMongoClient = AsyncMongoClient(settings.MONGO_URL)
        self.db = self.client[settings.MONGO_NAME]

    async def connect(self):
        await init_beanie(
            database=self.db,
            document_models=[User]
        )
        print(f"✅ Подключено к mongo db: {settings.MONGO_NAME}")

    def disconnect(self):
        if self.client:
            self.client.close()
            print(f"❌ Отключено от mongo db: {settings.MONGO_NAME}")

mongo_connector = MongoConnector()