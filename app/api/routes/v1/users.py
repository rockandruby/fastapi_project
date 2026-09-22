from fastapi import APIRouter, Depends, HTTPException
from app.database import get_session
from sqlmodel import Session, select
from app.models.user import User
import app.schemas.user as user_schema
from app.api.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[user_schema.UserIndex])
def read_users(session: Session = Depends(get_session)):
    statement = select(User)
    users = session.exec(statement).all()
    return users

@router.post("/", response_model=user_schema.UserCreate)
def create_user(user_data: user_schema.UserCreate,
                session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)):
    entry = User(**user_data.model_dump(exclude_unset=True))

    session.add(entry)
    session.commit()
    session.refresh(entry)

    return entry

@router.get("/{id}", response_model=user_schema.UserShow)
def show_user(id: int, session: Session = Depends(get_session)):
    entry = session.get(User, id)
    if not entry:
        raise HTTPException(status_code=404, detail="User not found")

    return entry

@router.patch("/{id}", response_model=user_schema.UserShow)
def update_user(id: int, user_data: user_schema.UserUpdate,
                session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)):
    entry = session.get(User, id)
    if not entry:
        raise HTTPException(status_code=404, detail="User not found")
    entry.sqlmodel_update(user_data.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(entry)

    return entry

@router.delete("/{id}")
def delete_user(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    entry = session.get(User, id)
    session.delete(entry)
    session.commit()