from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from core.auth import get_current_user
from core.logger import logger
from crud import create_item, delete_item, get_all_items, get_item, update_item
from models.engagement import Bookmark

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])
collection_name = "bookmarks"


@router.post("/")
async def create_bookmark(
    bookmark: Bookmark, current_user: dict = Depends(get_current_user)
):
    logger.info(f"Пользователь {current_user['user_uid']} создаёт закладку")

    if str(bookmark.user_uid) != str(current_user["user_uid"]):
        raise HTTPException(
            status_code=403,
            detail="Нельзя создать закладку от имени другого пользователя",
        )

    return await create_item(collection_name, bookmark.model_dump(exclude_unset=True))


@router.get("/", response_model=List[Bookmark])
async def list_bookmarks(current_user: dict = Depends(get_current_user)):
    logger.info(
        f"Пользователь {current_user['user_uid']} получает список своих закладок"
    )

    return await get_all_items(collection_name, UUID(current_user["user_uid"]))


@router.get("/{bookmark_id}", response_model=Bookmark)
async def get_bookmark(
    bookmark_id: UUID, current_user: dict = Depends(get_current_user)
):
    logger.info(
        f"Пользователь {current_user['user_uid']} получает закладку {bookmark_id}"
    )

    bookmark = await get_item(collection_name, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    if bookmark["user_uid"] != str(current_user["user_uid"]):
        raise HTTPException(status_code=403, detail="Нет доступа к этой закладке")

    return bookmark


@router.put("/{bookmark_id}", response_model=Bookmark)
async def update_bookmark(
    bookmark_id: UUID,
    bookmark: Bookmark,
    current_user: dict = Depends(get_current_user),
):
    logger.info(
        f"Пользователь {current_user['user_uid']} обновляет закладку {bookmark_id}"
    )

    existing = await get_item(collection_name, bookmark_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    if existing["user_uid"] != str(current_user["user_uid"]):
        raise HTTPException(
            status_code=403, detail="Нельзя редактировать чужую закладку"
        )

    return await update_item(
        collection_name, bookmark_id, bookmark.model_dump(exclude_unset=True)
    )


@router.delete("/{bookmark_id}")
async def delete_bookmark(
    bookmark_id: UUID, current_user: dict = Depends(get_current_user)
):
    logger.info(
        f"Пользователь {current_user['user_uid']} удаляет закладку {bookmark_id}"
    )

    existing = await get_item(collection_name, bookmark_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    if existing["user_uid"] != str(current_user["user_uid"]):
        raise HTTPException(status_code=403, detail="Нельзя удалить чужую закладку")

    await delete_item(collection_name, bookmark_id)
    return {"status": "deleted"}
