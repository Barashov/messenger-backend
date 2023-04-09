from fastapi import FastAPI
from core.database import database, engine, metadata


metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
