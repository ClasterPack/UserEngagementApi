from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException

from crud import create_item, get_all_items, update_item, get_item, delete_item
from models.engagement import Like
from main import logger

router = APIRouter(prefix="/likes", tags=["Likes"])
collection_name = "likes"


@router.post("/", response_model=Like)
async def create_like(like: Like):
    logger.info("запрос на создание like")
    result = await create_item(collection_name, like.model_dump(exclude_unset=True))
    return result


@router.get("/", response_model=List[Like])
async def list_likes(user_uid: Optional[UUID] = None):
    logger.info("запрос на получение списка like")

    return await get_all_items(collection_name, user_uid)


@router.get("/{like_id}", response_model=Like)
async def get_like(like_id: UUID):
    logger.info("запрос на получение like по id")

    like = await get_item(collection_name, like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    return like


@router.put("/{like_id}", response_model=Like)
async def update_like(like_id: UUID, like: Like):
    logger.info("запрос на изменение like по id")

    existing = await get_item(collection_name, like_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Like not found")

    result = await update_item(collection_name, like_id, like.model_dump(exclude_unset=True))
    return result


@router.delete("/{like_id}")
async def delete_like(like_id: UUID):
    logger.info("запрос на удаление like по id")

    deleted = await delete_item(collection_name, like_id)
    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Like not found")
    return {"status": "deleted"}
