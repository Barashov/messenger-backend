from pydantic import BaseModel


class ChatCreateOut(BaseModel):
    id: int
    name: str
    image: str | None
