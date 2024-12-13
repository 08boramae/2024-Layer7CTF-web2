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