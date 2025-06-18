from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends

from core.auth import get_current_user
from crud import create_item, get_all_items, update_item, get_item, delete_item
from models.engagement import Like
from core.logger import get_logger

router = APIRouter(prefix="/likes", tags=["Likes"])
collection_name = "likes"
logger = get_logger()


@router.post("/", response_model=Like)
async def create_like(
        like: Like,
        current_user: dict = Depends(get_current_user)):
    logger.info("запрос на создание like")
    if str(like.user_uid) != str(current_user["user_uid"]):
        raise HTTPException(status_code=403, detail="Нельзя ставить лайк от имени другого пользователя")
    result = await create_item(collection_name, like.model_dump(exclude_unset=True))
    return result


@router.get("/", response_model=List[Like])
async def list_likes(
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"Пользователь {current_user['user_uid']} запрашивает список своих лайков")

    return await get_all_items(collection_name, user_uid=UUID(current_user["user_uid"]))


@router.get("/{like_id}", response_model=Like)
async def get_like(
    like_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"Пользователь {current_user['user_uid']} запрашивает лайк {like_id}")

    like = await get_item(collection_name, like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    if like["user_uid"] != str(current_user["user_uid"]):
        raise HTTPException(status_code=403, detail="Нет доступа к этому лайку")

    return like


@router.put("/{like_id}", response_model=Like)
async def update_like(
    like_id: UUID,
    like: Like,
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"Пользователь {current_user['user_uid']} обновляет лайк {like_id}")

    existing = await get_item(collection_name, like_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Like not found")

    if existing["user_uid"] != str(current_user["user_uid"]):
        raise HTTPException(status_code=403, detail="Нельзя редактировать чужой лайк")

    result = await update_item(collection_name, like_id, like.model_dump(exclude_unset=True))
    return result


@router.delete("/{like_id}")
async def delete_like(
    like_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"Пользователь {current_user['user_uid']} удаляет лайк {like_id}")

    existing = await get_item(collection_name, like_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Like not found")

    if existing["user_uid"] != str(current_user["user_uid"]):
        raise HTTPException(status_code=403, detail="Нельзя удалить чужой лайк")

    await delete_item(collection_name, like_id)
    return {"status": "deleted"}
