from fastapi import FastAPI
from controller import auth, post, chat

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(post.router, prefix="/post", tags=["post"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])