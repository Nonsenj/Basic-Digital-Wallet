from httpx import AsyncClient
from backend import models
import pytest

@pytest.mark.asyncio
async def test_no_permission_create_wallets(
    client: AsyncClient, user1: models.DBUser
):
    payload = {"owner": "wallets", "user_id": user1.id}
    response = await client.post("/wallets", json=payload)

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_wallets(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"owner": "owners", "user_id": token_user1.user_id}
    response = await client.post("/wallets", json=payload, headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["owner"] == payload["owner"]
    assert data["id"] > 0
    assert data["user_id"] == token_user1.user_id

@pytest.mark.asyncio
async def test_update_wallets(
    client: AsyncClient, wallet_user1: models.DBWallet, token_user1: models.Token
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"owner": "test owners","balance": 50}

    response = await client.put(
        f"/wallets/{wallet_user1.id}", json=payload, headers=headers
    )

    data = response.json()

    assert response.status_code == 200
    

@pytest.mark.asyncio
async def test_list_wallets(client: AsyncClient, wallet_user1:models.DBWallet, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get("/wallets", headers=headers)

    data = response.json()
    assert response.status_code == 200
    assert len(data['wallets']) > 0
    check_wallet = None

    for wallet in data["wallets"]:
        assert wallet["user_id"] == token_user1.user_id

        if wallet["owner"] == wallet_user1.owner:
            check_wallet = wallet
            break

    assert check_wallet["id"] == wallet_user1.id
    assert check_wallet["owner"] == wallet_user1.owner

@pytest.mark.asyncio
async def test_delete_wallets(
    client: AsyncClient, wallet_user1: models.DBWallet, token_user1: models.Token,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}

    response = await client.delete(
        f"/wallets/{wallet_user1.id}", headers=headers
    )

    data = response.json()

    assert data == {"message": "delete success"}