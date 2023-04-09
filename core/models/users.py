from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import Table
from datetime import datetime
from core.database import metadata


users = Table('users',
              metadata,
              Column('id',
                     Integer,
                     primary_key=True),

              Column('username',
                     String,
                     unique=True,
                     index=True,
                     nullable=False),

              Column('email',
                     String,
                     unique=True,
                     index=True),

              Column('password',
                     String),

              Column('birthday',
                     DateTime),

              Column('created_at',
                     DateTime,
                     default=datetime.now()))


friends = Table('friends',
                metadata,
                Column('user_id', Integer, ForeignKey('users.id')),
                Column('friend_id', Integer, ForeignKey('users.id')))
