import pytest
from uuid import uuid4
from datetime import datetime, timezone


@pytest.mark.asyncio
async def test_create_review(client, test_user):
    payload = {
        "user_uid": test_user["user_uid"],
        "film_uid": str(uuid4()),
        "rating": 7,
        "description": "Очень понравился фильм"
    }
    response = await client.post("/reviews/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user_uid"] == test_user["user_uid"]
    assert "film_uid" in data
    assert "rating" in data
    assert "description" in data
    assert "_id" in data


@pytest.mark.asyncio
async def test_create_review_forbidden(client):
    payload = {
        "user_uid": str(uuid4()),
        "film_uid": str(uuid4()),
        "rating": 5,
        "description": "Некорректный отзыв"
    }
    response = await client.post("/reviews/", json=payload)
    assert response.status_code == 403
    assert response.json()["detail"] == "Нельзя создавать отзыв от имени другого пользователя"


@pytest.mark.asyncio
async def test_list_reviews(client, mock_reviews_crud, test_user):
    review_id = str(uuid4())
    mock_reviews_crud[review_id] = {
        "_id": review_id,
        "user_uid": test_user["user_uid"],
        "film_uid": str(uuid4()),
        "rating": 8,
        "description": "Отличный фильм",
        "created": datetime.now(timezone.utc).isoformat(),
        "modified": datetime.now(timezone.utc).isoformat(),
    }

    response = await client.get("/reviews/")
    assert response.status_code == 200
    reviews = response.json()
    assert isinstance(reviews, list)
    assert len(reviews) == 1
    assert reviews[0]["_id"] == review_id


@pytest.mark.asyncio
async def test_get_review(client, mock_reviews_crud, test_user):
    review_id = str(uuid4())
    film_uid = str(uuid4())
    mock_reviews_crud[review_id] = {
        "_id": review_id,
        "user_uid": test_user["user_uid"],
        "film_uid": film_uid,
        "rating": 9,
        "description": "Лучший фильм!",
        "created": datetime.now(timezone.utc).isoformat(),
        "modified": datetime.now(timezone.utc).isoformat(),
    }

    response = await client.get(f"/reviews/{review_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["film_uid"] == film_uid


@pytest.mark.asyncio
async def test_get_review_forbidden(client, mock_reviews_crud):
    review_id = str(uuid4())
    mock_reviews_crud[review_id] = {
        "_id": review_id,
        "user_uid": str(uuid4()),
        "film_uid": str(uuid4()),
        "rating": 4,
        "description": "Не мой отзыв",
        "created": datetime.now(timezone.utc).isoformat(),
        "modified": datetime.now(timezone.utc).isoformat(),
    }
    response = await client.get(f"/reviews/{review_id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Нет доступа к этому отзыву"


@pytest.mark.asyncio
async def test_update_review(client, mock_reviews_crud, test_user):
    review_id = str(uuid4())
    old_desc = "Старый отзыв"
    new_desc = "Обновленный отзыв"
    mock_reviews_crud[review_id] = {
        "_id": review_id,
        "user_uid": test_user["user_uid"],
        "film_uid": str(uuid4()),
        "rating": 5,
        "description": old_desc,
        "created": datetime.now(timezone.utc).isoformat(),
        "modified": datetime.now(timezone.utc).isoformat(),
    }

    updated_data = {
        "user_uid": test_user["user_uid"],
        "film_uid": mock_reviews_crud[review_id]["film_uid"],
        "rating": 6,
        "description": new_desc,
    }

    response = await client.put(f"/reviews/{review_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == new_desc
    assert data["rating"] == 6


@pytest.mark.asyncio
async def test_update_review_forbidden(client, mock_reviews_crud):
    review_id = str(uuid4())
    mock_reviews_crud[review_id] = {
        "_id": review_id,
        "user_uid": str(uuid4()),
        "film_uid": str(uuid4()),
        "rating": 2,
        "description": "Отзыв другого пользователя",
        "created": datetime.now(timezone.utc).isoformat(),
        "modified": datetime.now(timezone.utc).isoformat(),
    }

    updated_data = {
        "user_uid": mock_reviews_crud[review_id]["user_uid"],
        "film_uid": mock_reviews_crud[review_id]["film_uid"],
        "rating": 3,
        "description": "Попытка обновить чужой отзыв",
    }
    response = await client.put(f"/reviews/{review_id}", json=updated_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Нельзя редактировать чужой отзыв"


@pytest.mark.asyncio
async def test_delete_review(client, mock_reviews_crud, test_user):
    review_id = str(uuid4())
    mock_reviews_crud[review_id] = {
        "_id": review_id,
        "user_uid": test_user["user_uid"],
        "film_uid": str(uuid4()),
        "rating": 7,
        "description": "Отзыв для удаления",
        "created": datetime.now(timezone.utc).isoformat(),
        "modified": datetime.now(timezone.utc).isoformat(),
    }

    response = await client.delete(f"/reviews/{review_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "deleted"}


@pytest.mark.asyncio
async def test_delete_review_forbidden(client, mock_reviews_crud):
    review_id = str(uuid4())
    mock_reviews_crud[review_id] = {
        "_id": review_id,
        "user_uid": str(uuid4()),
        "film_uid": str(uuid4()),
        "rating": 1,
        "description": "Чужой отзыв",
        "created": datetime.now(timezone.utc).isoformat(),
        "modified": datetime.now(timezone.utc).isoformat(),
    }

    response = await client.delete(f"/reviews/{review_id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "You can only delete your own reviews."
