from fastapi import APIRouter, Response, status, Depends
from controller.auth import get_current_user
from dao import database
from typing import Annotated


router = APIRouter()

@router.get("/")
def index(response: Response):
    response.status_code = status.HTTP_200_OK
    return {"status": "200", "message": "OK"}

@router.get("/<chat_id>")
def get_chat(response: Response, chat_id: int):
    # TODO
    return 1

@router.post("/<chat_id>")
def post_chat(response: Response, chat_id: int):
    # TODO
    return 1