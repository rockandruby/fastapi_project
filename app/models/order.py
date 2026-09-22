from sqlmodel import SQLModel, Field, Relationship, Column, DateTime
from datetime import datetime
from typing import TYPE_CHECKING
from app.api.helpers import current_time

if TYPE_CHECKING:
    from app.models.user import User

class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    title: str
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

    user: User = Relationship(back_populates="orders")

