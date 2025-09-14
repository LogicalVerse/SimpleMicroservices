from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated, Optional

UNIType = Annotated[str, StringConstraints(pattern=r"^[a-z]{2,3}\d{1,4}$")]


class HobbiesBase(BaseModel):
    Name: str = Field(description="Full name of the student")
    UNI: UNIType = Field(description="University ID")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    Hobbies: list[str] = Field(description="List of hobbies")

    model_config = {
        "json_schema_extra": {
            "example": {
                "Name": "Ayush Verma",
                "UNI": "av3334",
                "timestamp": "2025-09-02T12:34:56Z",
                "Hobbies": ["Gym", "Reading", "Traveling"]
            }
        }
    }


class HobbiesCreate(HobbiesBase):
    """Creation payload for a Student's hobbies."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Name": "Ayush Verma",
                    "UNI": "av3334",
                    "timestamp": "2025-09-02T12:34:56Z",
                    "Hobbies": ["Gym", "Reading", "Traveling"]
                }
            ]
        }
    }


class HobbiesUpdate(BaseModel):
    """Partial update for a Student's hobbies; supply only fields to change."""
    Name: Optional[str] = Field(None, json_schema_extra={"example": "Ayush"})
    UNI: Optional[UNIType] = Field(
        None, description="Columbia UNI.", json_schema_extra={"example": "ab1234"}
    )
    Hobbies: Optional[list[str]] = Field(
        None, json_schema_extra={"example": ["Photography", "Music"]}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Name": "Updated Name",
                    "UNI": "xy123",
                    "Hobbies": ["Photography", "Music"]
                }
            ]
        }
    }


class HobbiesRead(HobbiesBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Student ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "99999999-9999-4999-8999-999999999999",
                    "Name": "Ayush Verma",
                    "UNI": "av3334",
                    "timestamp": "2025-09-02T12:34:56Z",
                    "Hobbies": ["Gym", "Reading", "Traveling"],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
