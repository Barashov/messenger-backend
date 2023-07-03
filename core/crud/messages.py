from sqlalchemy import select, desc

from core.database import database
from core.models.messages import messages
from core.models.users import users
from core.models.chats import chats


async def create_message(text, user_id, chat_id):
    query = messages.insert().values(text=text,
                                     sent_by=user_id,
                                     to_chat=chat_id)
    message = await database.execute(query)
    return message


async def get_messages(chat_id, limit, offset):
    select_fields = [
        messages.c.id.label('id'),
        messages.c.text.label('text'),
        messages.c.created_at.label('created_at'),
        users.c.id.label('user_id'),
        users.c.username.label('username'),
    ]

    query = select(select_fields)\
        .join_from(messages, users)\
        .join(chats, messages.c.to_chat == chats.c.id)\
        .where(chats.c.id == chat_id)\
        .order_by(desc(messages.c.id))\
        .limit(limit)\
        .offset(offset)
    return await database.fetch_all(query)

