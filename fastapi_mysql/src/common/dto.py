from pydantic import BaseModel


class DeleteResponse(BaseModel):
    detail: str


class UpdatedResponse(BaseModel):
    detail: str
