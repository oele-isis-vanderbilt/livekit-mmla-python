import asyncio

import pytest

from livekit_mmla.client import LiveKitMMLAClient

loop: asyncio.AbstractEventLoop


@pytest.mark.asyncio(scope="module")
async def test_remember_loop():
    global loop
    loop = asyncio.get_running_loop()


@pytest.fixture(scope="module")
def client():

    return LiveKitMMLAClient(project="test")


def test_get_api_token(client):
    token = client.api_token
    assert token is not None


@pytest.mark.asyncio(scope="module")
async def test_get_livekit_token(client):
    token = await client.get_livekit_token("test", "test", create_room=True)
    assert token is not None


@pytest.mark.asyncio(scope="module")
async def test_create_room(client):
    room = await client.create_room("test")
    assert room is not None
    assert room.name == "test"


@pytest.mark.asyncio(scope="module")
async def test_list_rooms(client):
    rooms = await client.list_rooms()
    assert rooms is not None
    assert len(rooms) > 0
    assert rooms[0].name is not None
