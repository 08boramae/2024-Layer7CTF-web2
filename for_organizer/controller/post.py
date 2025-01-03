from http.client import HTTPException

from fastapi import APIRouter, Response, status, Depends
from typing import Annotated
from dao import database
from model import model
from controller.auth import get_current_user

router = APIRouter()

@router.get("/")
def index(response: Response):
    response.status_code = status.HTTP_200_OK
    return {"status": "200", "message": "OK"}

@router.get("/list")
async def post_list(response: Response, current_user: Annotated[dict, Depends(get_current_user)]):
    posts = database.list_post()
    response.status_code = status.HTTP_200_OK
    return {"status": "200", "message": "OK", "posts": posts}

@router.post("/insert")
async def post_insert(response: Response, data: model.PostInsert, current_user: Annotated[dict, Depends(get_current_user)]):
    try:
        database.insert_post(current_user['id'], current_user['name'], data.content)
        response.status_code = status.HTTP_201_CREATED
        return {"status": "201", "message": "Created"}
    except:
        raise HTTPException(status_code=400, detail="Bad Request")
