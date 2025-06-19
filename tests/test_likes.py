from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_create_like(client, test_user):
    payload = {"user_uid": str(test_user["user_uid"]), "film_uid": str(uuid4())}
    response = await client.post("/likes/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user_uid"] == str(test_user["user_uid"])
    assert "_id" in data



@pytest.mark.asyncio
async def test_list_likes(client, mock_likes_crud, test_user):
    like_id = str(uuid4())
    mock_likes_crud[like_id] = {
        "_id": like_id,
        "user_uid": str(test_user["user_uid"]),
        "film_uid": str(uuid4()),
        "created": "2025-06-19T20:20:38.843199",
        "modified": "2025-06-19T20:20:38.843200",
    }

    response = await client.get("/likes/")
    assert response.status_code == 200
    likes = response.json()
    assert isinstance(likes, list)
    assert any(like.get("_id") == like_id for like in likes)


@pytest.mark.asyncio
async def test_get_like(client, mock_likes_crud, test_user):
    like_id = str(uuid4())
    film_uid = str(uuid4())
    mock_likes_crud[like_id] = {
        "_id": like_id,
        "user_uid": str(test_user["user_uid"]),
        "film_uid": film_uid,
        "created": "2025-06-19T20:20:38.843199",
        "modified": "2025-06-19T20:20:38.843200",
    }

    response = await client.get(f"/likes/{like_id}")
    assert response.status_code == 200
    data = response.json()
    assert "_id" in data and data["_id"] == like_id
    if "film_uid" in data:
        assert data["film_uid"] == film_uid


@pytest.mark.asyncio
async def test_update_like(client, mock_likes_crud, test_user):
    like_id = str(uuid4())
    old_film_uid = str(uuid4())
    new_film_uid = str(uuid4())

    mock_likes_crud[like_id] = {
        "_id": like_id,
        "user_uid": str(test_user["user_uid"]),
        "film_uid": old_film_uid,
        "created": "2025-06-19T20:20:38.843199",
        "modified": "2025-06-19T20:20:38.843200",
    }

    updated_data = {"user_uid": str(test_user["user_uid"]), "film_uid": new_film_uid}

    response = await client.put(f"/likes/{like_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    if "film_uid" in data:
        assert data["film_uid"] == new_film_uid
    assert data["_id"] == like_id


@pytest.mark.asyncio
async def test_delete_like(client, mock_likes_crud, test_user):
    like_id = str(uuid4())
    mock_likes_crud[like_id] = {
        "_id": like_id,
        "user_uid": str(test_user["user_uid"]),
        "film_uid": str(uuid4()),
        "created": "2025-06-19T20:20:38.843199",
        "modified": "2025-06-19T20:20:38.843200",
    }

    response = await client.delete(f"/likes/{like_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "deleted"}
