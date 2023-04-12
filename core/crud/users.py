from core.database import database
from core.models.users import users


async def is_username_taken(username) -> bool:
    query = users.select().where(users.c.username == username)
    result = await database.fetch_one(query)
    return bool(result)


async def create_user(username, hashed_password):
    query = users.insert().values(username=username,
                                  password=hashed_password)
    return await database.execute(query)


async def get_user_by_username(username: str):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)


async def get_user_by_email(email: str):
    query = users.select().where(users.c.email == email)
    return await database.fetch_one(query)

