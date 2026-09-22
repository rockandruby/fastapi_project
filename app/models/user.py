from sqlmodel import SQLModel, Field, Relationship, Column, DateTime
from datetime import datetime
from typing import TYPE_CHECKING
from app.api.helpers import current_time

if TYPE_CHECKING:
    from app.models.order import Order

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=current_time,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )
    updated_at: datetime = Field(
        default_factory=current_time,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            onupdate=current_time,
        ),
    )

    orders: list[Order] = Relationship(back_populates="user")

