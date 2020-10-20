import pytest
from channels.testing import WebsocketCommunicator

from .consumers import StreamConsumer


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_auth_with_bad_token():
    communicator = WebsocketCommunicator(StreamConsumer, "/ws/streams/")
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.send_json_to(data={"cmd": "auth", "token": "bad-auth-token"})
    response = await communicator.receive_json_from()
    assert response["code"] == 400
    # Close
    await communicator.disconnect()


# Here transaction=True is necessary: https://github.com/django/channels/issues/1110
@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_auth_with_valid_token(admin_user):
    communicator = WebsocketCommunicator(StreamConsumer, "/ws/streams/")
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.send_json_to(
        data={"cmd": "auth", "token": admin_user.auth_token.key}
    )
    response = await communicator.receive_json_from()
    assert response["code"] == 200
    assert communicator.scope["user"] == admin_user
    # Close
    await communicator.disconnect()


# https://github.com/django/channels/issues/1343
@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_already_auth(admin_user):
    communicator = WebsocketCommunicator(StreamConsumer, "/ws/streams/")
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.send_json_to(
        data={"cmd": "auth", "token": admin_user.auth_token.key}
    )
    response = await communicator.receive_json_from()
    assert response["code"] == 200
    assert communicator.scope["user"] == admin_user

    await communicator.send_json_to(
        data={"cmd": "auth", "token": admin_user.auth_token.key}
    )
    with pytest.raises(AssertionError):
        await communicator.receive_from()

    # Close
    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_sub_private_topics_without_auth():
    communicator = WebsocketCommunicator(StreamConsumer, "/ws/streams/")
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.send_json_to(data={"cmd": "sub", "topics": ["robot#1.log"]})
    response = await communicator.receive_json_from()
    assert response["code"] == 401

    # Close
    await communicator.disconnect()


@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_sub_private_topics_with_auth(admin_user):
    communicator = WebsocketCommunicator(StreamConsumer, "/ws/streams/")
    connected, subprotocol = await communicator.connect()
    assert connected

    await communicator.send_json_to(
        data={"cmd": "auth", "token": admin_user.auth_token.key}
    )
    response = await communicator.receive_json_from()
    assert response["code"] == 200
    assert communicator.scope["user"] == admin_user

    await communicator.send_json_to(data={"cmd": "sub", "topics": ["robot#1.log"]})
    with pytest.raises(AssertionError):
        await communicator.receive_from()

    # Close
    await communicator.disconnect()
