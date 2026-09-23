from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from app.database import get_session
from sqlmodel import Session
from typing import Annotated
import jwt
from datetime import datetime, timezone, timedelta
from app.settings import SECRET_KEY, ALGORITHM
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SessionDep = Annotated[Session, Depends(get_session)]

def sync_http_client(request: Request):
    return request.app.state.sync_client

def async_http_client(request: Request):
    return request.app.state.async_client

def create_access_token(user_id, expires_in: int = 3600):
    expire = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(access_token):
    try:
        return jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        return None

def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="User not authorized")

    user_id = payload["sub"]
    user = session.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not authorized")

    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]