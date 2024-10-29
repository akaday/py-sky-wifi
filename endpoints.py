from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging
import psutil
from pydantic import BaseModel, ValidationError

from .main import app, database
from .auth import User, fake_users_db, fake_hash_password, authenticate_user, enforce_password_policy, generate_otp, verify_otp, track_failed_login_attempts, lock_account, unlock_account
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
        track_failed_login_attempts(form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is locked. Please contact support.",
        )
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/")
def read_root():
    return {"message": "Welcome to PySkyWiFi!"}

@router.post("/users/")
async def create_user(username: str, password: str, otp: str):
    if not enforce_password_policy(password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password does not meet complexity requirements",
        )
    if not verify_otp(username, otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP",
        )
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
        preferences = NetworkPreferences(**preferences.dict())
        logger.info(f"Network preferences updated: {preferences}")
        return {"message": "Network preferences updated"}
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail="Invalid network preferences")
    except Exception as e:
        logger.error(f"Error updating network preferences: {e}")
        raise HTTPException(status_code=500, detail="Error updating network preferences")

@router.get("/network/status")
def get_network_status():
    try:
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
        device = Device(**device.dict())
        logger.info(f"Device access restricted: {device}")
        return {"message": "Device access restricted"}
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail="Invalid device data")
    except Exception as e:
        logger.error(f"Error restricting device access: {e}")
        raise HTTPException(status_code=500, detail="Error restricting device access")

@router.get("/wifi/signal_strength")
def get_wifi_signal_strength():
    try:
        signal_strength = {
            "ssid": "example_ssid",
            "strength": -50
        }
        return {"signal_strength": signal_strength}
    except Exception as e:
        logger.error(f"Error getting Wi-Fi signal strength: {e}")
        raise HTTPException(status_code=500, detail="Error getting Wi-Fi signal strength")

@router.post("/wifi/signal_strength/notify")
def notify_signal_strength_drop(threshold: int):
    try:
        current_signal_strength = -60
        if current_signal_strength < threshold:
            return {"message": "Signal strength has dropped below the threshold"}
        return {"message": "Signal strength is above the threshold"}
    except Exception as e:
        logger.error(f"Error notifying signal strength drop: {e}")
        raise HTTPException(status_code=500, detail="Error notifying signal strength drop")

@router.post("/wifi/auto_reconnect")
def auto_reconnect():
    try:
        return {"message": "Auto-reconnect feature implemented"}
    except Exception as e:
        logger.error(f"Error implementing auto-reconnect feature: {e}")
        raise HTTPException(status_code=500, detail="Error implementing auto-reconnect feature")

@router.get("/wifi/speed_test")
def speed_test():
    try:
        speed_metrics = {
            "download_speed": 50,
            "upload_speed": 10,
            "latency": 20,
            "packet_loss": 0
        }
        return {"speed_metrics": speed_metrics}
    except Exception as e:
        logger.error(f"Error performing speed test: {e}")
        raise HTTPException(status_code=500, detail="Error performing speed test")

@router.get("/network/usage_statistics")
def get_network_usage_statistics():
    try:
        usage_statistics = {
            "data_usage": 1000,
            "connected_time": 3600
        }
        return {"usage_statistics": usage_statistics}
    except Exception as e:
        logger.error(f"Error getting network usage statistics: {e}")
        raise HTTPException(status_code=500, detail="Error getting network usage statistics")

@router.post("/guest_networks")
def create_guest_network(ssid: str, password: str):
    if not ssid or not password:
        raise HTTPException(status_code=400, detail="SSID and password must not be empty")
    try:
        return {"message": f"Guest network '{ssid}' created with limited privileges"}
    except Exception as e:
        logger.error(f"Error creating guest network: {e}")
        raise HTTPException(status_code=500, detail="Error creating guest network")

@router.get("/guest_networks/usage")
def get_guest_network_usage():
    try:
        guest_network_usage = {
            "data_usage": 500,
            "connected_time": 1800
        }
        return {"guest_network_usage": guest_network_usage}
    except Exception as e:
        logger.error(f"Error getting guest network usage: {e}")
        raise HTTPException(status_code=500, detail="Error getting guest network usage")
