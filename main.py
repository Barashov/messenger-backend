from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import database, engine, metadata
from routers.users import router as users_router
from routers.chats import router as chats_router


metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router, prefix='/users', tags=['users'])
app.include_router(chats_router, prefix='/chats', tags=['chats'])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
