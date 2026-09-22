from sqlmodel import SQLModel
from datetime import datetime

class UserCreate(SQLModel):
    name: str
    email: str
    password: str

class UserIndex(SQLModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

class UserShow(UserIndex):
    orders: list[OrderShow]

class UserUpdate(SQLModel):
    name: str

# Order
class OrderShow(SQLModel):
    title: str
    created_at: datetime
    updated_at: datetime

class UserLogin(SQLModel):
    email: str
    password: str
