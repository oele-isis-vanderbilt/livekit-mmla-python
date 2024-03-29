import os
import time
from typing import List

import httpx
import jwt

from .models import (
    ApiToken,
    CreateRoomRequest,
    LiveKitRoom,
    RoomOptions,
    TokenRequest,
    VideoGrants,
)


class LiveKitMMLAClient:
    def __init__(
        self, *, api_key=None, api_secret=None, server_url=None, project=None
    ):
        self.api_key = api_key or os.getenv("LIVEKIT_MMLA_API_KEY")
        self.api_secret = api_secret or os.getenv("LIVEKIT_MMLA_API_SECRET")
        self.server_url = server_url or os.getenv("LIVEKIT_MMLA_SERVER_URL")
        self.project = project or os.getenv("LIVEKIT_MMLA_PROJECT")
        if not self.api_key:
            raise ValueError(
                "api_key is required, please provide it or set LIVEKIT_MMLA_API_KEY environment variable"
            )
        if not self.api_secret:
            raise ValueError(
                "api_secret is required, please provide it or set LIVEKIT_MMLA_API_SECRET environment variable"
            )
        if not self.server_url:
            raise ValueError(
                "server_url is required, please provide it or set LIVEKIT_MMLA_SERVER_URL environment variable"
            )

        self.httpx_client = httpx.AsyncClient(base_url=self.server_url)
        self._api_token = None

    @property
    def api_token(self):
        if not self._api_token:
            self._api_token = self.get_api_token()
        if self.is_expired(self._api_token):
            self._api_token = self.get_api_token()
        return self._api_token

    def get_api_token(self) -> str:
        api_token = ApiToken(
            iat=int(time.time()),
            exp=int(time.time()) + 60 * 60,
            iss=self.api_key,
            project=self.project,
        )
        encoded_jwt = jwt.encode(
            api_token.model_dump(mode="json", by_alias=True),
            self.api_secret,
            algorithm="HS256",
        )
        return encoded_jwt

    def is_expired(self, token):
        decoded_jwt = jwt.decode(token, self.api_secret, algorithms=["HS256"])
        api_token = ApiToken(**decoded_jwt)
        return api_token.is_expired()

    async def get_livekit_token(
        self,
        room_name,
        identity,
        is_subscriber=False,
        create_room=False,
        **room_create_kwargs,
    ) -> str:
        if create_room:
            await self.create_room(room_name, **room_create_kwargs)

        grants = VideoGrants()
        grants.room = room_name
        grants.can_publish = True
        grants.can_subscribe = is_subscriber
        grants.can_publish_data = True

        token_request = TokenRequest(identity=identity, video_grants=grants)
        result = await self._authenticated_post(
            "/livekit/token",
            json=token_request.model_dump(mode="json", by_alias=True),
        )
        result.raise_for_status()
        return result.json()["token"]

    async def list_rooms(self) -> List[LiveKitRoom]:
        result = await self._authenticated_get("/livekit/list-rooms")
        result.raise_for_status()
        return [LiveKitRoom(**room) for room in result.json()]

    async def create_room(
        self, room_name, empty_timeout=600, max_participants=100, metadata=""
    ) -> LiveKitRoom:
        room_request = CreateRoomRequest(
            name=room_name,
            options=RoomOptions(
                empty_timeout=empty_timeout,
                max_participants=max_participants,
                metadata=metadata,
            ),
        )
        result = await self._authenticated_post(
            "/livekit/create-room",
            json=room_request.model_dump(mode="json", by_alias=True),
        )
        result.raise_for_status()
        return LiveKitRoom(**result.json())

    async def _authenticated_post(
        self, url, json=None, headers=None
    ) -> httpx.Response:
        headers = headers or {}
        if json is None:
            json = {}
        headers["Authorization"] = f"Bearer {self.api_token}"
        result = await self.httpx_client.post(url, json=json, headers=headers)
        return result

    async def _authenticated_get(self, url, headers=None) -> httpx.Response:
        headers = headers or {}
        headers["Authorization"] = f"Bearer {self.api_token}"
        result = await self.httpx_client.get(url, headers=headers)
        return result
