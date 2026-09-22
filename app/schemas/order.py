from sqlmodel import SQLModel
from datetime import datetime

class OrderCreate(SQLModel):
    title: str

class OrderIndex(SQLModel):
    title: str
    created_at: datetime
    updated_at: datetime

class OrderShow(OrderIndex):
    user: UserShow

class OrderUpdate(SQLModel):
    title: str

# User
class UserShow(SQLModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
