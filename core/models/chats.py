from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, ForeignKey
from core.database import metadata


chats = Table(
    'chats',
    metadata,

    Column('id',
           Integer,
           primary_key=True),

    Column('name',
           String,
           nullable=False),

    Column('created_by',
           Integer,
           ForeignKey('users.id')),

    Column('image',
           String),

)


chat_users = Table(
    'chat_users',
    metadata,

    Column('chat_id',
           Integer,
           ForeignKey('chats.id')),

    Column('user_id',
           Integer,
           ForeignKey('users.id'))
)
