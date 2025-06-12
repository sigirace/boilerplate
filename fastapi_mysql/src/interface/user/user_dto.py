from typing import List
from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):

    email: EmailStr = Field(
        max_length=64,
    )
    name: str = Field(
        min_length=2,
        max_length=32,
    )
    password: str = Field(
        min_length=4,
        max_length=32,
    )


class UserResponse(BaseModel):

    id: str
    email: str
    name: str


class UserListRequest(BaseModel):

    page: int = Field(
        default=1,
    )
    item_per_page: int = Field(
        default=10,
    )


class UserListResponse(BaseModel):

    page: int
    total_count: int
    users: List[UserResponse]


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        max_length=64,
    )
    password: str = Field(
        min_length=4,
        max_length=32,
    )


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(
        default="bearer",
    )
