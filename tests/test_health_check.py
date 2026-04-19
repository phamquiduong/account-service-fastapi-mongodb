import pytest


@pytest.mark.anyio
async def test_health_check(client):
    res = await client.get("/")
    assert res.json() == {"status": "ok"}
    assert res.status_code == 200
