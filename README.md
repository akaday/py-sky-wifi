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
