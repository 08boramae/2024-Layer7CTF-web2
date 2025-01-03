from fastapi import APIRouter, Response, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from dao import database
from model import model
import jwt
from typing import Annotated
import os

router = APIRouter()

SECRET_KEY = os.urandom(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return payload


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get("/")
def index(response: Response):
    response.status_code = status.HTTP_200_OK
    return {"status": "200", "message": "OK"}


@router.post("/register")
def register(response: Response, data: model.Register):
    try:
        database.insert_user(data.name, data.id, data.password)
        response.status_code = status.HTTP_201_CREATED
        return {"status": "201", "message": "Created"}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "400", "message": "Bad Request"}


@router.post("/login")
def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = database.login(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=401, detail='Unauthorized')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"uid": user[0], "id": user[1], "name": user[3]},
        expires_delta=access_token_expires
    )

    response.status_code = status.HTTP_200_OK
    return {
        "status": "200",
        "message": "OK",
        "access_token": access_token,
        "token_type": "bearer"
    }