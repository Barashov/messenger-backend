from pydantic import BaseModel, constr


class UserCreate(BaseModel):
    username: constr(min_length=3)
    password: constr(min_length=4)


class UserLogin(BaseModel):
    name: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    token: str
