from fastapi import APIRouter, Response, status, Depends, HTTPException
from controller.auth import get_current_user
from dao import database
from typing import Annotated
from model.model import *
from fastapi.responses import HTMLResponse

router = APIRouter()

chat_draft = ""

@router.get("/list")
def list_chats(response: Response, current_user: Annotated[dict, Depends(get_current_user)]):
    chats = database.get_user_chats(current_user["uid"])
    response.status_code = status.HTTP_200_OK
    data = {
        "status": "200",
        "message": "OK",
        "data": chats
    }
    return HTMLResponse(content=str(data), status_code=200)

@router.post("/create")
def create_chat(response: Response, chat_data: CreateChatRoom, current_user: Annotated[dict, Depends(get_current_user)]):
    # 생성자를 멤버 목록에 추가
    members = list(set(chat_data.members + [current_user["uid"]]))
    chat_id = database.create_chat_room(
        chat_data.room_name,
        chat_data.room_type,
        current_user["uid"],
        members
    )

    response.status_code = status.HTTP_201_CREATED
    data = {
        "status": "201",
        "message": "Chat room created successfully",
        "data": {"chat_id": chat_id}
    }
    return HTMLResponse(content=str(data), status_code=201)

@router.get("/{chat_id}")
def get_chat(response: Response, chat_id: int, current_user: Annotated[dict, Depends(get_current_user)], draft: str = None):
    chat_data = database.get_chat(chat_id, current_user["uid"])
    response.status_code = status.HTTP_200_OK
    data = {
        "status": "200",
        "message": "OK",
        "draft": draft,
        "data": chat_data
    }
    return HTMLResponse(content=str(data), status_code=200)

@router.post("/{chat_id}")
def post_chat(response: Response, chat_id: int, message: ChatMessage, current_user: Annotated[dict, Depends(get_current_user)]):
    message_id = database.post_chat(chat_id, current_user["uid"], message.content)
    response.status_code = status.HTTP_201_CREATED
    data = {
        "status": "201",
        "message": "Message posted successfully",
        "data": {"message_id": message_id}
    }
    return HTMLResponse(content=str(data), status_code=201)