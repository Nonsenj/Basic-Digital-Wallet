from httpx import AsyncClient
from backend import models
import pytest

@pytest.mark.asyncio
async def test_say_wallet(client: AsyncClient):
    print("Hello wallet") 