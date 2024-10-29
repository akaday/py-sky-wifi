from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging

from .main import app, database
from .auth import User, fake_users_db, fake_hash_password, authenticate_user
from app.wifi import scan_wifi, connect_to_wifi

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/")
def read_root():
    return {"message": "Welcome to PySkyWiFi!"}

@router.post("/users/")
async def create_user(username: str, password: str):
    query = users.insert().values(username=username, password=fake_hash_password(password))
    await database.execute(query)
    return {"username": username}

@router.get("/wifi/scan")
def scan_wifi_networks():
    try:
        networks = scan_wifi()
        return {"networks": networks}
    except Exception as e:
        logger.error(f"Error scanning Wi-Fi networks: {e}")
        raise HTTPException(status_code=500, detail="Error scanning Wi-Fi networks")

@router.post("/wifi/connect")
def connect_to_wifi_network(ssid: str, password: str):
    if not ssid or not password:
        raise HTTPException(status_code=400, detail="SSID and password must not be empty")
    try:
        connect_to_wifi(ssid, password)
        return {"message": "Connected to Wi-Fi network"}
    except Exception as e:
        logger.error(f"Error connecting to Wi-Fi network: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to Wi-Fi network")
