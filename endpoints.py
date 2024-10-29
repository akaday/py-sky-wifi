from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .main import app, database
from .auth import User, fake_users_db, fake_hash_password, authenticate_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
