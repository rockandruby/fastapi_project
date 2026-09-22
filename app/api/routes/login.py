from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
import app.schemas.user as user_schema
from pwdlib import PasswordHash
from app.api.deps import create_access_token

router = APIRouter(tags=["login"])

@router.post("/login")
def login(user_data: user_schema.UserLogin, session: Session = Depends(get_session),):
    password_hash = PasswordHash.recommended()
    statement = select(User).where(User.email == user_data.email)
    user = session.exec(statement).first()
    if not user or not password_hash.verify(user_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    return create_access_token(user.id)
