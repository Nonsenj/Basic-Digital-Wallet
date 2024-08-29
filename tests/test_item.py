from httpx import AsyncClient
from backend import models
import pytest

@pytest.mark.asyncio
async def test_no_permission_create_items(
    client: AsyncClient, user1: models.DBUser
):
    payload = {"name": "items", "user_id": user1.id}
    response = await client.post("/items", json=payload)

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_items(client: AsyncClient, token_user1: models.Token, merchant_user1: models.DBMerchant):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"name": "items", "user_id": token_user1.user_id, "merchant_id": merchant_user1.id}
    response = await client.post("/items", json=payload, headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == payload["name"]
    assert data["id"] > 0
    assert data["user_id"] == token_user1.user_id
    assert data["merchant_id"] == merchant_user1.id

@pytest.mark.asyncio
async def test_update_items(
    client: AsyncClient, item_user1: models.DBItem, token_user1: models.Token, merchant_user1: models.DBMerchant,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"name": "test item name", "merchant_id": merchant_user1.id}

    response = await client.put(
        f"/items/{item_user1.id}", json=payload, headers=headers
    )

    data = response.json()
    print(data)

    assert response.status_code == 200
    assert data["name"] == payload["name"]
    assert data["id"] == item_user1.id

@pytest.mark.asyncio
async def test_list_items(client: AsyncClient, item_user1: models.DBItem):
    response = await client.get("/items")

    data = response.json()
    assert response.status_code == 200
    assert len(data['items']) > 0
    check_item = None

    for item in data["items"]:
        if item["name"] == item_user1.name:
            check_item = item
            break

    assert check_item["id"] == item_user1.id
    assert check_item["name"] == item_user1.name

@pytest.mark.asyncio
async def test_delete_items(
    client: AsyncClient, item_user1: models.DBItem, token_user1: models.Token,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}

    response = await client.delete(
        f"/items/{item_user1.id}", headers=headers
    )

    data = response.json()

    assert data == {"message": "delete success"}