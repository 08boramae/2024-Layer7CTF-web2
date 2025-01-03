from pydantic import BaseModel

class Isauth(BaseModel):
    token: str

class Register(BaseModel):
    id: str
    password: str
    name: str

class Login(BaseModel):
    id: str
    password: str

class PostInsert(BaseModel):
    content: str

class ChatMessage(BaseModel):
    content: str

class CreateChatRoom(BaseModel):
    room_name: str
    room_type: str
    members: list[int]

class BotLocation(BaseModel):
    location: str
