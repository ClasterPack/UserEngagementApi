from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_create_bookmark(client, test_user):
    payload = {"user_uid": test_user["user_uid"], "film_uid": str(uuid4())}
    response = await client.post("/bookmarks/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user_uid"] == test_user["user_uid"]
    assert "film_uid" in data
    assert "_id" in data


@pytest.mark.asyncio
async def test_list_bookmarks(client, mock_bookmarks_crud, test_user):
    bookmark_id = str(uuid4())
    mock_bookmarks_crud[bookmark_id] = {
        "_id": bookmark_id,
        "user_uid": test_user["user_uid"],
        "film_uid": str(uuid4()),
        "created": "2025-06-19T20:20:38.843199",
        "modified": "2025-06-19T20:20:38.843200",
    }

    response = await client.get("/bookmarks/")
    assert response.status_code == 200
    bookmarks = response.json()
    assert isinstance(bookmarks, list)
    assert len(bookmarks) == 1
    assert bookmarks[0]["_id"] == bookmark_id


@pytest.mark.asyncio
async def test_get_bookmark(client, mock_bookmarks_crud, test_user):
    bookmark_id = str(uuid4())
    film_uid = str(uuid4())
    mock_bookmarks_crud[bookmark_id] = {
        "_id": bookmark_id,
        "user_uid": test_user["user_uid"],
        "film_uid": film_uid,
        "created": "2025-06-19T20:20:38.843199",
        "modified": "2025-06-19T20:20:38.843200",
    }

    response = await client.get(f"/bookmarks/{bookmark_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["film_uid"] == film_uid


@pytest.mark.asyncio
async def test_update_bookmark(client, mock_bookmarks_crud, test_user):
    bookmark_id = str(uuid4())
    old_film_uid = str(uuid4())
    new_film_uid = str(uuid4())

    mock_bookmarks_crud[bookmark_id] = {
        "_id": bookmark_id,
        "user_uid": test_user["user_uid"],
        "film_uid": old_film_uid,
        "created": "2025-06-19T20:20:38.843199",
        "modified": "2025-06-19T20:20:38.843200",
    }

    updated_data = {"user_uid": test_user["user_uid"], "film_uid": new_film_uid}

    response = await client.put(f"/bookmarks/{bookmark_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["film_uid"] == new_film_uid


@pytest.mark.asyncio
async def test_delete_bookmark(client, mock_bookmarks_crud, test_user):
    bookmark_id = str(uuid4())
    mock_bookmarks_crud[bookmark_id] = {
        "_id": bookmark_id,
        "user_uid": test_user["user_uid"],
        "film_uid": str(uuid4()),
        "created": "2025-06-19T20:20:38.843199",
        "modified": "2025-06-19T20:20:38.843200",
    }

    response = await client.delete(f"/bookmarks/{bookmark_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "deleted"}
