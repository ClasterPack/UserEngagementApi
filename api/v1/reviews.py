from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException

from crud import create_item, delete_item, get_all_items, get_item, update_item
from models.engagement import Review
from main import logger

router = APIRouter(prefix="/reviews", tags=["Reviews"])
collection_name = "reviews"


@router.post("/", response_model=Review)
async def create_review(review: Review):
    logger.info("запрос на создание review")

    result = await create_item(
        collection_name,
        review.model_dump(exclude_unset=True)
    )
    return result


@router.get("/", response_model=List[Review])
async def list_reviews(user_uid: Optional[UUID] = None):
    logger.info("запрос на получение всех review")

    return await get_all_items(collection_name, user_uid)


@router.get("/{review_id}", response_model=Review)
async def get_review(review_id: UUID):
    logger.info("запрос на получение review по id")

    review = await get_item(collection_name, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.put("/{review_id}", response_model=Review)
async def update_review(review_id: UUID, review: Review):
    logger.info("запрос на изменение review")

    existing = await get_item(collection_name, review_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Review not found")

    result = await update_item(collection_name, review_id, review.model_dump(exclude_unset=True))
    return result


@router.delete("/{review_id}")
async def delete_review(review_id: UUID):
    logger.info("запрос на удаление review")

    deleted = await delete_item(collection_name, review_id)
    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"status": "deleted"}
