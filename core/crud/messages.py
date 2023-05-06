from core.database import database
from core.models.messages import messages


async def create_message(text, user_id, chat_id):
    query = messages.insert().values(text=text,
                                     sent_by=user_id,
                                     to_chat=chat_id)
    message = await database.execute(query)

    print(dir(message))
    return message
