from typing import List, Optional
from pydantic import BaseModel, Field


from common.models import Lifecycle, ListObjects
from utils.crypto import Crypto
import ulid


class Profile(BaseModel):
    name: str
    email: str


class User(BaseModel):
    id: str
    profile: Profile
    password: str
    lifecycle: Lifecycle

    @classmethod
    def create(
        cls,
        name: str,
        email: str,
        password: str,
    ) -> "User":

        return cls(
            id=str(str(ulid.new())),
            profile=Profile(name=name, email=email),
            password=password,
            lifecycle=Lifecycle(),
        )


class UserList(ListObjects):
    users: List[User]
