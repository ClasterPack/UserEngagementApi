from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends

from core.auth import get_current_user
from crud import create_item, delete_item, get_all_items, get_item, update_item
from models.engagement import Review
from core.logger import get_logger

router = APIRouter(prefix="/reviews", tags=["Reviews"])
collection_name = "reviews"
logger = get_logger()


@router.post("/", response_model=Review)
async def create_review(
    review: Review,
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"Пользователь {current_user['user_uid']} создаёт review")

    if str(review.user_uid) != str(current_user["user_uid"]):
        raise HTTPException(status_code=403, detail="Нельзя создавать отзыв от имени другого пользователя")

    result = await create_item(collection_name, review.model_dump(exclude_unset=True))
    return result


@router.get("/", response_model=List[Review])
async def list_reviews(
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"Пользователь {current_user['user_uid']} получает список своих отзывов")

    return await get_all_items(collection_name, UUID(current_user["user_uid"]))


@router.get("/{review_id}", response_model=Review)
async def get_review(
    review_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"Пользователь {current_user['user_uid']} запрашивает отзыв {review_id}")

    review = await get_item(collection_name, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review["user_uid"] != str(current_user["user_uid"]):
        raise HTTPException(status_code=403, detail="Нет доступа к этому отзыву")

    return review


@router.put("/{review_id}", response_model=Review)
async def update_review(
    review_id: UUID,
    review: Review,
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"Пользователь {current_user['user_uid']} редактирует отзыв {review_id}")

    existing = await get_item(collection_name, review_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Review not found")

    if existing["user_uid"] != str(current_user["user_uid"]):
        raise HTTPException(status_code=403, detail="Нельзя редактировать чужой отзыв")

    result = await update_item(collection_name, review_id, review.model_dump(exclude_unset=True))
    return result


@router.delete("/{review_id}")
async def delete_review(
    review_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"Пользователь {current_user['user_uid']} удаляет отзыв {review_id}")

    existing = await get_item(collection_name, review_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Review not found")

    if existing["user_uid"] != str(current_user["user_uid"]):
        raise HTTPException(status_code=403, detail="You can only delete your own reviews.")

    await delete_item(collection_name, review_id)
    return {"status": "deleted"}
