# PySkyWiFi

## Overview
**PySkyWiFi** is a WiFi login system for airline websites using Python and FastAPI. This system provides secure login, session management, and user registration.

## Features
- Secure user authentication
- User registration with strong password policies
- Multi-factor authentication (MFA) for user registration
- Account lockout mechanisms
- Session management
- Database integration with SQLAlchemy
- Configure network preferences
- Display real-time network status and statistics
- Log network events and activities
- Send alerts for important network events
- Manage connected devices

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/akaday/py-sky-wifi.git
   cd py-sky-wifi
   ```

## Endpoints

### User Authentication
- **POST /token**: Authenticate user and return access token.
- **POST /users/**: Create a new user with OTP verification.

### WiFi Management
- **GET /wifi/scan**: Scan for available WiFi networks.
- **POST /wifi/connect**: Connect to a WiFi network.
- **GET /wifi/signal_strength**: Get the signal strength of the current WiFi network.
- **POST /wifi/signal_strength/notify**: Notify when WiFi signal strength drops below a threshold.
- **POST /wifi/auto_reconnect**: Enable auto-reconnect feature for WiFi.
- **GET /wifi/speed_test**: Perform a speed test on the current WiFi network.

### Network Preferences
- **POST /network/preferences**: Configure network preferences.
- **GET /network/status**: Get the current network status.
- **GET /network/usage_statistics**: Get network usage statistics.

### Device Management
- **GET /devices**: List all connected devices.
- **POST /devices/restrict**: Restrict access for a specific device.

### Guest Networks
- **POST /guest_networks**: Create a guest network with limited privileges.
- **GET /guest_networks/usage**: Get usage statistics for the guest network.

## User Registration and Authentication

### User Registration
To register a new user, follow these steps:
1. Generate an OTP for the user by calling the `generate_otp` function.
2. Send the OTP to the user via email or SMS.
3. Call the `register_user` function with the username, password, and OTP to complete the registration process.

### User Authentication
To authenticate a user, follow these steps:
1. Call the `authenticate_user` function with the username and password.
2. If the authentication is successful, an access token will be returned.
3. Use the access token to access protected endpoints.
####
allowing users to update their website URL via Wi-Fi while on a plane. This involves providing an endpoint that users can access to modify the website URL. The script we previously created, update_website.py, now integrated into endpoints.py, is a perfect example of how to do this.

Here is a quick review of how this works:

Key Components in endpoints.py
1. Endpoint to Update the Website URL: This allows users to modify the website URL through an HTTP PUT request.

python
Copier
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()

class WebsiteUpdateRequest(BaseModel):
    new_url: str

current_website = {
    "url": "http://example.com"
}

@router.put("/update_website/")
async def update_website(request: WebsiteUpdateRequest):
    if not request.new_url:
        raise HTTPException(status_code=400, detail="New URL must be provided")
    current_website["url"] = request.new_url
    return {"message": "Website URL updated successfully", "new_url": current_website["url"]}
2. Endpoint to Get the Current Website URL: This provides users with the current URL via an HTTP GET request.

python
Copier
@router.get("/current_website/")
async def get_current_website():
    return {"current_url": current_website["url"]}
3. Integrating into the FastAPI Application: Ensure these endpoints are included in your main FastAPI application setup.

python
Copier
from fastapi import FastAPI
from .endpoints import router as endpoints_router

app = FastAPI()

app.include_router(endpoints_router)
How to Use:
Get the Current URL:

bash
Copier
curl -X GET "http://127.0.0.1:8000/current_website/"
This will return the current website URL.

Update the Website URL:

bash
Copier
curl -X PUT "http://127.0.0.1:8000/update_website/" -H "Content-Type: application/json" -d '{"new_url": "http://new-website-url.com"}'
This will update the URL to the new value provided.

Deployment Considerations:
Security: Ensure that these endpoints are secure, especially if used over public or insecure networks. Implement authentication and authorization to restrict access.

Logging and Monitoring: Track changes and monitor usage to detect any unauthorized changes or issues.

Error Handling: Implement robust error handling to manage invalid inputs or other issues gracefully.

This setup allows users to update their website URL dynamically, even while connected through Wi-Fi on a plane, provided they have the necessary access to the endpoints.

If you have any more features or improvements in mind, or need further assistance, just let me know! 😊🚀✨
