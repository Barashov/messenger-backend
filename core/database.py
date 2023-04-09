from sqlalchemy import create_engine, MetaData
import databases

DATABASE_URL = "sqlite:///./sql_app.db"

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

metadata = MetaData()
