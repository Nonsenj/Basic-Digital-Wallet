from httpx import AsyncClient
from backend import models
import pytest

@pytest.mark.asyncio
async def test_no_permission_create_transactions(
    client: AsyncClient, user1: models.DBUser, item_user1: models.DBItem
):
    payload = {"item_id": item_user1.id, "user_id": user1.id}
    response = await client.post("/transactions", json=payload)

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_transactions(
    client: AsyncClient, 
    token_user1: models.Token, 
    item_user1: models.DBItem,
    merchant_user1: models.DBMerchant,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"item_id": item_user1.id, "merchant_id": merchant_user1.id, "user_id": token_user1.user_id}
    response = await client.post("/transactions", json=payload, headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["id"] > 0
    assert data["user_id"] == token_user1.user_id
    assert data["item_id"] == item_user1.id
    assert data["merchant_id"] == merchant_user1.id

# @pytest.mark.asyncio
# async def test_update_transactions(
#     client: AsyncClient, 
#     token_user1: models.Token, 
#     item_user1: models.DBItem,
#     merchant_user1: models.DBMerchant,
#     transaction_user1: models.DBTransaction
# ):
#     headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
#     payload = {"amount": 20, "item_id": item_user1.id, "merchant_id": merchant_user1.id, "user_id": token_user1.user_id}

#     response = await client.put(
#         f"/transactions/{transaction_user1.id}", json=payload, headers=headers
#     )

#     data = response.json()

#     assert response.status_code == 200
#     assert data["amount"] == 20
#     assert data["id"] == transaction_user1.id
    

@pytest.mark.asyncio
async def test_list_transactions(
    client: AsyncClient, 
    token_user1: models.Token,
    item_user1: models.DBItem,
    merchant_user1: models.DBMerchant, 
    transaction_user1: models.DBTransaction
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get("/transactions", headers=headers)

    data = response.json()
    assert response.status_code == 200
    assert len(data['transactions']) > 0
    check_transaction = None

    for transaction in data["transactions"]:
        # assert wallet["user_id"] == token_user1.user_id

        if transaction["amount"] == transaction_user1.amount:
            check_transaction = transaction
            break

    assert check_transaction["id"] == transaction_user1.id
    assert check_transaction["amount"] == 10
    assert check_transaction["item_id"] == item_user1.id
    assert check_transaction["merchant_id"] == merchant_user1.id

@pytest.mark.asyncio
async def test_delete_transactions(
    client: AsyncClient, transaction_user1: models.DBTransaction, token_user1: models.Token,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}

    response = await client.delete(
        f"/transactions/{transaction_user1.id}", headers=headers
    )

    data = response.json()

    assert data == {"message": "delete success"}