from fastapi import FastAPI
from app.routers import swift
from app.database import Base, engine


app = FastAPI()

app.include_router(
    swift.router,
    prefix="/v1",
)


@app.get("/")
def welcome_page():
    return {"Hi": "Welcome"}


Base.metadata.create_all(bind=engine)
