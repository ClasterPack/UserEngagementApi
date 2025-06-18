from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from fastapi.encoders import jsonable_encoder

from core.db import mongo_db


async def create_item(collection_name: str, data: dict):
    if not data.get("id"):
        data["id"] = uuid4()

    now = datetime.now()
    data["created"] = now
    data["modified"] = now

    data = jsonable_encoder(data)

    await mongo_db[collection_name].insert_one(data)
    return await mongo_db[collection_name].find_one({"id": str(data["id"])}, {"_id": 0})


async def get_item(collection_name: str, item_id: UUID):
    return await mongo_db[collection_name].find_one({"id": str(item_id)}, {"_id": 0})


async def get_all_items(collection_name: str, user_uid: Optional[UUID] = None):
    query = {}
    if user_uid:
        query["user_uid"] = str(user_uid)
    cursor = mongo_db[collection_name].find(query, {"_id": 0})
    return [doc async for doc in cursor]


async def update_item(collection_name: str, item_id: UUID, data: dict):
    data["modified"] = datetime.now()
    data = jsonable_encoder(data)

    await mongo_db[collection_name].update_one({"id": str(item_id)}, {"$set": data})
    return await get_item(collection_name, item_id)


async def delete_item(collection_name: str, item_id: UUID):
    return await mongo_db[collection_name].delete_one({"id": str(item_id)})
