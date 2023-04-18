from core.crud.chats import get_chat_by_id


async def is_user_chat_creator(chat_id, user_id):
    chat = await get_chat_by_id(chat_id)
    return chat.created_by == user_id
