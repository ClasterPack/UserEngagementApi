import pytest
from fastapi import Depends
from httpx import ASGITransport, AsyncClient

from api.v1 import bookmarks as bookmarks_crud
from api.v1 import likes as likes_crud
from api.v1 import reviews as reviews_crud
from api.v1.bookmarks import get_current_user as original_get_current_user
from core.auth import oauth2_scheme
from main import app


@pytest.fixture
def test_user():
    return {"user_uid": str(uuid4())}


from datetime import datetime, timezone
from uuid import uuid4


def create_mock_crud(monkeypatch, crud_module, collection_name):
    fake_db = {}

    async def mock_create_item(collection, data):
        if collection != collection_name:
            raise ValueError(
                f"Unexpected collection {collection}, expected {collection_name}"
            )

        item = data.copy()
        item["_id"] = str(uuid4())
        now = datetime.now(timezone.utc).isoformat()
        item["created"] = now
        item["modified"] = now

        fake_db[item["_id"]] = item
        return item

    async def mock_get_item(collection, item_id):
        if collection != collection_name:
            raise ValueError(
                f"Unexpected collection {collection}, expected {collection_name}"
            )
        return fake_db.get(str(item_id))

    async def mock_get_all_items(collection, user_uid=None):
        if collection != collection_name:
            raise ValueError(
                f"Unexpected collection {collection}, expected {collection_name}"
            )
        if user_uid:
            return [
                item for item in fake_db.values() if item["user_uid"] == str(user_uid)
            ]
        return list(fake_db.values())

    async def mock_update_item(collection, item_id, data):
        if collection != collection_name:
            raise ValueError(
                f"Unexpected collection {collection}, expected {collection_name}"
            )
        if str(item_id) in fake_db:
            fake_db[str(item_id)].update(data)
            fake_db[str(item_id)]["modified"] = datetime.now(timezone.utc).isoformat()
            return fake_db[str(item_id)]
        return None

    async def mock_delete_item(collection, item_id):
        if collection != collection_name:
            raise ValueError(
                f"Unexpected collection {collection}, expected {collection_name}"
            )
        return fake_db.pop(str(item_id), None)

    monkeypatch.setattr(crud_module, "create_item", mock_create_item)
    monkeypatch.setattr(crud_module, "get_item", mock_get_item)
    monkeypatch.setattr(crud_module, "get_all_items", mock_get_all_items)
    monkeypatch.setattr(crud_module, "update_item", mock_update_item)
    monkeypatch.setattr(crud_module, "delete_item", mock_delete_item)

    return fake_db


@pytest.fixture(autouse=True)
def override_get_current_user(test_user):
    async def mock_get_current_user(token: str = Depends(oauth2_scheme)):
        return test_user

    app.dependency_overrides[original_get_current_user] = mock_get_current_user
    yield
    app.dependency_overrides.pop(original_get_current_user, None)


@pytest.fixture(autouse=True)
def mock_bookmarks_crud(monkeypatch):
    return create_mock_crud(monkeypatch, bookmarks_crud, "bookmarks")


@pytest.fixture(autouse=True)
def mock_likes_crud(monkeypatch):
    return create_mock_crud(monkeypatch, likes_crud, "likes")

@pytest.fixture(autouse=True)
def mock_reviews_crud(monkeypatch):
    return create_mock_crud(monkeypatch, reviews_crud, "reviews")


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    headers = {"Authorization": "Bearer faketoken123"}
    async with AsyncClient(
        transport=transport, base_url="http://test", headers=headers
    ) as ac:
        yield ac
