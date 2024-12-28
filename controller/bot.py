# admin only
from datetime import timedelta

from fastapi import APIRouter, Response, status, Depends, HTTPException
from controller.auth import get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import urllib

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 1
@router.get("/")
def index(response: Response):
    response.status_code = status.HTTP_200_OK
    return {"status": "200", "message": "OK"}

@router.post('/submit')
def submit(response: Response, current_user: dict = Depends(get_current_user), location: str = None):
    if current_user['id'] != 'admin':
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"status": "401", "message": "Unauthorized"}
    # try:
    check(location)
    response.status_code = status.HTTP_200_OK
    return {"status": "200", "message": "OK"}
    # except Exception as e:
    #     response.status_code = status.HTTP_400_BAD_REQUEST
    #     return {"status": "400", "message": str(e)}

def read_url(url):
    service = Service(executable_path="/chromedriver")
    options = webdriver.ChromeOptions()
    for _ in [
        "headless",
        "window-size=1920x1080",
        "disable-gpu",
        "no-sandbox",
        "disable-dev-shm-usage",
    ]:
        options.add_argument(_)
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.implicitly_wait(3)
        driver.set_page_load_timeout(3)
        driver.get("http://127.0.0.1:8000/")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"uid": 0, "id": "bot", "name": "bot"},
            expires_delta=access_token_expires
        )
        driver.add_cookie({"name": "Authorization", "value": f"Bearer {access_token}"})
        driver.get(url)
    except Exception as e:
        driver.quit()
        return False
    driver.quit()
    return True

def check(location):
    filtered_location = filter(location)
    url = f"http://127.0.0.1:8000/{urllib.parse.quote(filtered_location)}"
    return read_url(url)

def filter(text):
    keyword = ["script", "on", "javascript", "window", "self", "this", "document", "location", "(", ")", "&#"]
    for f in keyword:
        if f in text.lower():
            return "NOPE"
    return text