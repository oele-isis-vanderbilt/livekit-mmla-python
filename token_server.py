from functools import lru_cache
from typing import Any, Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.alias_generators import to_camel
from pydantic_settings import BaseSettings, SettingsConfigDict

from livekit_mmla.client import LiveKitMMLAClient


class AppConfig(BaseSettings):
    livekit_mmla_server_url: str
    livekit_mmla_api_key: str
    livekit_mmla_api_secret: str
    livekit_mmla_project: Optional[str]

    model_config = SettingsConfigDict(env_file="livekit-mmla/.env")


@lru_cache
def get_settings():
    return AppConfig()


settings = get_settings()
mmla_client = LiveKitMMLAClient(
    server_url=settings.livekit_mmla_server_url,
    api_key=settings.livekit_mmla_api_key,
    api_secret=settings.livekit_mmla_api_secret,
    project=settings.livekit_mmla_project,
)

app = FastAPI()


class TokenRequest(BaseModel):
    identity: str
    room_name: str

    model_config = {
        "alias_generator": to_camel,
        "populate_by_name": True,
    }


@app.post("/token")
async def generate_token(token_request: TokenRequest) -> Dict[str, Any]:
    return {
        "token": await mmla_client.get_livekit_token(
            token_request.room_name, token_request.identity, create_room=True
        )
    }
