from sqlalchemy import Table, Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from core.database import metadata


messages = Table(
    'messages',
    metadata,

    Column('id',
           Integer,
           primary_key=True),

    Column('text',
           Text),

    Column('sent_by',
           Integer,
           ForeignKey('users.id')),

    Column('to_chat',
           Integer,
           ForeignKey('chats.id')),

    Column('created_at',
           DateTime,
           default=func.now())
)
