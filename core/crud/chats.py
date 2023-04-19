from sqlalchemy import and_, select
from core.database import database
from core.models.chats import chats, chat_users
from core.models.users import users


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


async def get_list_of_chat_users(chat_id):
    select_fields = [users.c.id,
                     users.c.username]
    query = select(select_fields).join(chat_users).where(chat_users.c.chat_id == chat_id)
    return await database.fetch_all(query)


async def get_chat_by_id(chat_id):

    query = chats.select().where(chats.c.id == chat_id)
    return await database.fetch_one(query)


async def delete_user_from_chat(chat_id, user_id):
    query = chat_users.delete().where(and_(chat_users.c.chat_id == chat_id,
                                           chat_users.c.user_id == user_id))
    await database.execute(query)


async def delete_chat(chat_id):
    query = chats.delete().where(chats.c.id == chat_id)
    await database.execute(query)


async def get_user_chats(user_id):
    select_fields = [chats.c.id,
                     chats.c.name,
                     chats.c.created_by,
                     chats.c.image]
    query = select(select_fields).join(chat_users).where(chat_users.c.user_id == user_id)
    return await database.fetch_all(query)
