from core.database import database
from core.models.chats import chats


async def create_chat(name: str,
                      created_by: int,
                      image: str = None):

    query = chats.insert().values(name=name,
                                  created_by=created_by,
                                  image=image)

    return await database.execute(query)
