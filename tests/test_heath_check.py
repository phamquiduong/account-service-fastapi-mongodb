import pytest


@pytest.mark.anyio
async def test_root(client):
    res = await client.get("/")
    assert res.json() == {"status": "ok"}
    assert res.status_code == 200
