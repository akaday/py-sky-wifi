from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging
import psutil
from pydantic import BaseModel

from .main import app, database
from .auth import User, fake_users_db, fake_hash_password, authenticate_user
from app.wifi import scan_wifi, connect_to_wifi

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NetworkPreferences(BaseModel):
    ssid: str
    password: str

class Device(BaseModel):
    name: str
    mac_address: str

connected_devices = []

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

@router.post("/network/preferences")
def configure_network_preferences(preferences: NetworkPreferences):
    try:
        # Here you would add the logic to configure network preferences
        logger.info(f"Network preferences updated: {preferences}")
        return {"message": "Network preferences updated"}
    except Exception as e:
        logger.error(f"Error updating network preferences: {e}")
        raise HTTPException(status_code=500, detail="Error updating network preferences")

@router.get("/network/status")
def get_network_status():
    try:
        # Here you would add the logic to get real-time network status and statistics
        network_status = {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent
        }
        return {"network_status": network_status}
    except Exception as e:
        logger.error(f"Error getting network status: {e}")
        raise HTTPException(status_code=500, detail="Error getting network status")

@router.get("/devices")
def list_connected_devices():
    try:
        return {"devices": connected_devices}
    except Exception as e:
        logger.error(f"Error listing connected devices: {e}")
        raise HTTPException(status_code=500, detail="Error listing connected devices")

@router.post("/devices/restrict")
def restrict_device_access(device: Device):
    try:
        # Here you would add the logic to restrict device access
        logger.info(f"Device access restricted: {device}")
        return {"message": "Device access restricted"}
    except Exception as e:
        logger.error(f"Error restricting device access: {e}")
        raise HTTPException(status_code=500, detail="Error restricting device access")
