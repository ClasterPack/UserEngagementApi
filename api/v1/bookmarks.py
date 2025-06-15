from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException

from crud import create_item, delete_item, get_all_items, get_item, update_item
from models.engagement import Bookmark

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])
collection_name = "bookmarks"


@router.post("/")
async def create_bookmark(bookmark: Bookmark):
    return await create_item(collection_name, bookmark.model_dump(exclude_unset=True))


@router.get("/", response_model=List[Bookmark])
async def list_bookmarks(user_uid: Optional[UUID] = None):
    return await get_all_items(collection_name, user_uid)


@router.get("/{bookmark_id}", response_model=Bookmark)
async def get_bookmark(bookmark_id: UUID):
    bookmark = await get_item(collection_name, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@router.put("/{bookmark_id}", response_model=Bookmark)
async def update_bookmark(bookmark_id: UUID, bookmark: Bookmark):
    existing = await get_item(collection_name, bookmark_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    result = await update_item(collection_name, bookmark_id, bookmark.model_dump(exclude_unset=True))
    return result


@router.delete("/{bookmark_id}")
async def delete_bookmark(bookmark_id: UUID):
    deleted = await delete_item(collection_name, bookmark_id)
    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return {"status": "deleted"}
