from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, StringConstraints

from .address import AddressBase

UNIType = Annotated[str, StringConstraints(pattern=r"^[a-z]{2,3}\d{1,4}$")]


class StudentBase(BaseModel):
    uni: UNIType = Field(
        ...,
        description="Columbia University UNI (2–3 lowercase letters + 1–4 digits).",
        json_schema_extra={"example": "av3334"},
    )
    first_name: str = Field(
        ...,
        description="Given name.",
        json_schema_extra={"example": "Ayush"},
    )
    last_name: str = Field(
        ...,
        description="Family name.",
        json_schema_extra={"example": "Verma"},
    )
    degree: str = Field(
        ...,
        description="Degree Type.",
        json_schema_extra={"example": "MS"},
    )
    field: str = Field(
        ...,
        description="Field of Study.",
        json_schema_extra={"example": "Computer Science"},
    )
    email: EmailStr = Field(
        ...,
        description="Primary email address.",
        json_schema_extra={"example": "av3334@columbia.edu"},
    )
    phone: Optional[str] = Field(
        None,
        description="Contact phone number in any reasonable format.",
        json_schema_extra={"example": "+1-212-555-0199"},
    )
    birth_date: Optional[date] = Field(
        None,
        description="Date of birth (YYYY-MM-DD).",
        json_schema_extra={"example": "2002-03-27"},
    )

    addresses: List[AddressBase] = Field(
        default_factory=list,
        description="Addresses linked to this student (each carries a persistent Address ID).",
        json_schema_extra={
            "example": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "street": "123 St",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10027",
                    "country": "USA",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uni": "av3334",
                    "first_name": "Ayush",
                    "last_name": "Verma",
                    "degree": "MS",
                    "field": "Computer Science",
                    "email": "av3334@columbia.edu",
                    "phone": "+1-212-555-0199",
                    "birth_date": "2002-03-27",
                    "addresses": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "street": "123 St",
                            "city": "New York",
                            "state": "NY",
                            "postal_code": "10027",
                            "country": "USA",
                        }
                    ],
                }
            ]
        }
    }


class StudentCreate(StudentBase):
    """Creation payload for a Student."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uni": "av3334",
                    "first_name": "Ayush",
                    "last_name": "Verma",
                    "degree": "MS",
                    "field": "Computer Science",
                    "email": "av3334@columbia.edu",
                    "phone": "+1-212-555-0199",
                    "birth_date": "2002-03-27",
                    "addresses": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "street": "123 St",
                            "city": "New York",
                            "state": "NY",
                            "postal_code": "10027",
                            "country": "USA",
                        }
                    ],
                }
            ]
        }
    }


class StudentUpdate(BaseModel):
    """Partial update for a Student; supply only fields to change."""
    uni: Optional[UNIType] = Field(
        None, description="Columbia UNI.", json_schema_extra={"example": "ab1234"}
    )
    first_name: Optional[str] = Field(None, json_schema_extra={"example": "Ayush"})
    last_name: Optional[str] = Field(None, json_schema_extra={"example": "Verma"})
    degree: Optional[str] = Field(None, json_schema_extra={"example": "PhD"})
    field: Optional[str] = Field(None, json_schema_extra={"example": "Data Science"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "av3334@columbia.edu"})
    phone: Optional[str] = Field(None, json_schema_extra={"example": "+1-212-555-0199"})
    birth_date: Optional[date] = Field(None, json_schema_extra={"example": "1815-12-10"})
    addresses: Optional[List[AddressBase]] = Field(
        None,
        description="Replace the entire set of addresses with this list.",
        json_schema_extra={
            "example": [
                {
                    "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                    "street": "123 St",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10027",
                    "country": "USA",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"first_name": "Ayush", "last_name": "Verma"},
                {"phone": "+1-415-555-0199"},
                {"degree": "PhD", "field": "Data Science"},
                {
                    "addresses": [
                        {
                            "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                            "street": "123 St",
                            "city": "New York",
                            "state": "NY",
                            "postal_code": "10027",
                            "country": "USA",
                        }
                    ]
                },
            ]
        }
    }


class StudentRead(StudentBase):
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
                    "uni": "av3334",
                    "first_name": "Ayush",
                    "last_name": "Verma",
                    "degree": "MS",
                    "field": "Computer Science",
                    "email": "av3334@columbia.edu",
                    "phone": "+1-212-555-0199",
                    "birth_date": "2002-03-27",
                    "addresses": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "street": "123 St",
                            "city": "New York",
                            "state": "NY",
                            "postal_code": "10027",
                            "country": "USA",
                        }
                    ],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
