from fastapi import FastAPI
from routes import public
from database.quiz_db import database, metadata, engine
from internal.crud import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.include_router(
    public.route,
    prefix="/public",
    tags=["public"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def __run_before_start__():
    await database.connect()
    metadata.create_all(engine)


@app.on_event("shutdown")
async def __run_before_start__():
    await database.disconnect()
