import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated, Optional

UNIType = Annotated[str, StringConstraints(pattern=r"^[a-z]{2,3}\d{1,4}$")]


class CoursesBase(BaseModel):
    Name: str = Field(description="Full name of the student")
    UNI: UNIType = Field(description="University ID")
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    Courses: list[str] = Field(description="List of enrolled courses")

    model_config = {
        "json_schema_extra": {
            "example": {
                "Name": "Ayush Verma",
                "UNI": "av3334",
                "timestamp": "2025-09-02T12:34:56Z",
                "Courses": ["Cloud Computing", "NLP", "AI"]
            }
        }
    }


class CoursesCreate(CoursesBase):
    """Creation payload for a Student."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Name": "Ayush Verma",
                    "UNI": "av3334",
                    "timestamp": "2025-09-02T12:34:56Z",
                    "Courses": ["Cloud Computing", "NLP", "AI"]
                }
            ]
        }
    }


class CoursesUpdate(BaseModel):
    """Partial update for the Courses; supply only fields to change."""
    Name: Optional[str] = Field(None, json_schema_extra={"example": "Ayush"})
    UNI: Optional[UNIType] = Field(
        None, description="Columbia UNI.", json_schema_extra={"example": "ab1234"}
    )
    Courses: Optional[list[str]] = Field(
        None, json_schema_extra={"example": ["AI", "ML"]}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Name": "Updated Name",
                    "UNI": "xy123",
                    "Courses": ["AI", "ML"]
                }
            ]
        }
    }


class CoursesRead(CoursesBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Student ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
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
                    "Courses": ["Cloud Computing", "NLP", "AI"],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
