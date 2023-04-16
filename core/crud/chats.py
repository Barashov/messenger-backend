from sqlalchemy import and_
from core.database import database
from core.models.chats import chats, chat_users


async def create_chat(name: str,
                      created_by: int,
                      image: str = None):

    query = chats.insert().values(name=name,
                                  created_by=created_by,
                                  image=image)

    return await database.execute(query)


async def add_user_to_chat(chat_id, user_id):
    query = chat_users.insert().values(chat_id=chat_id, user_id=user_id)
    await database.execute(query)


async def is_user_in_chat(chat_id, user_id):
    query = chat_users.select().where(and_(chat_users.c.chat_id == chat_id,
                                           chat_users.c.user_id == user_id))
    return await database.fetch_one(query)
