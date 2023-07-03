from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    id: int
    text: str
    created_at: datetime | None
    user_id: int
    username: str

    class Config:
        orm_mode = True
