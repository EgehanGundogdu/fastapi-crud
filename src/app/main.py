from fastapi import FastAPI

from app.api import user_router

app = FastAPI()


@app.get("/")
def ping():
    return {"ping": "pong"}


app.include_router(user_router, tags=["users"])
