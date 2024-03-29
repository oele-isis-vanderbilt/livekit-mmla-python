import time
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


class VideoGrants(BaseModel):
    room_create: bool = Field(False, description="Allow creating rooms")
    room_list: bool = Field(False, description="Allow listing rooms")
    room_record: bool = Field(False, description="Allow recording rooms")

    room_admin: bool = Field(
        False, description="Allow admin operations on rooms"
    )
    room_join: bool = Field(False, description="Allow joining rooms")
    room: str = Field("", description="Room name")

    can_publish: bool = Field(False, description="Allow publishing tracks")
    can_subscribe: bool = Field(
        False, description="Allow subscribing to tracks"
    )
    can_publish_data: bool = Field(
        False, description="Allow publishing data tracks"
    )

    can_publish_sources: List[str] = Field(
        [], description="Allow publishing sources"
    )

    can_update_own_metadata: bool = Field(
        False, description="Allow updating own metadata"
    )

    ingress_admin: bool = Field(
        False, description="Allow admin operations on ingress"
    )

    hidden: bool = Field(False, description="Hide the room from list")
    recorder: bool = Field(False, description="Is room recorder")

    model_config = {
        "alias_generator": to_camel,
        "populate_by_name": True,
    }


class TokenRequest(BaseModel):
    identity: str = Field(..., description="Identity of the user")
    video_grants: Optional[VideoGrants] = Field(
        default=None, description="Video grants"
    )

    model_config = {
        "alias_generator": to_camel,
        "populate_by_name": True,
    }


class ApiToken(BaseModel):
    iat: int = Field(description="Issued at")
    exp: int = Field(description="Expiration time")
    iss: str = Field(description="Issuer")

    project: Optional[str] = Field(description="Project name")

    model_config = {
        "alias_generator": to_camel,
        "populate_by_name": True,
    }

    def is_expired(self) -> bool:
        return self.exp < int(time.time())


class RoomOptions(BaseModel):
    empty_timeout: int = Field(
        600, description="Timeout in seconds to delete empty room"
    )
    max_participants: int = Field(
        100, description="Maximum number of participants"
    )
    metadata: str = Field("", description="Room metadata")

    model_config = {
        "alias_generator": to_camel,
        "populate_by_name": True,
    }


class CreateRoomRequest(BaseModel):
    name: str = Field(..., description="Name of the room")
    options: Optional[RoomOptions] = Field(
        default=None, description="Room options"
    )

    model_config = {
        "alias_generator": to_camel,
        "populate_by_name": True,
    }


class LiveKitRoom(BaseModel):
    sid: str = Field(description="Room SID")
    name: str = Field(description="Room name")
    empty_timeout: int = Field(description="Empty timeout")
    max_participants: int = Field(description="Max participants")
    creation_time: int = Field(description="Creation time")
    turn_password: str = Field(description="TURN password")
    enabled_codecs: List[str] = Field(description="Enabled codecs")
    metadata: str = Field(description="Metadata")
    num_participants: int = Field(description="Number of participants")
    num_publishers: int = Field(description="Number of publishers")
    active_recording: bool = Field(description="Active recording")

    model_config = {
        "alias_generator": to_camel,
        "populate_by_name": True,
    }
