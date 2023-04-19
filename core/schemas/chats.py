from pydantic import BaseModel


class ChatCreateOut(BaseModel):
    id: int
    name: str
    image: str | None


class FullChat(BaseModel):
    id: int
    name: str
    created_by: int
    image: str | None

    class Config:
        orm_mode = True
