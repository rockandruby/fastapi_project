from fastapi import APIRouter, Depends, HTTPException
from app.database import get_session
from sqlmodel import Session, select
from app.models.order import Order
from app.models.user import User
import app.schemas.order as order_schema
from app.api.deps import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=list[order_schema.OrderShow])
def read_orders(session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)):
    orders = session.scalars(select(Order).where(Order.user_id == current_user.id))
    return orders

@router.post("/", response_model=order_schema.OrderShow)
def create_order(order_data: order_schema.OrderCreate,
                 session: Session = Depends(get_session),
                 current_user: User = Depends(get_current_user)):
    entry = Order(**order_data.model_dump(exclude_unset=True))
    entry.user_id = current_user.id

    session.add(entry)
    session.commit()
    session.refresh(entry)

    return entry

@router.get("/{id}", response_model=order_schema.OrderShow)
def show_order(id: int,
               session: Session = Depends(get_session),
               current_user: User = Depends(get_current_user)):
    order = session.scalar(
        select(Order).where(Order.id == id, Order.user_id == current_user.id)
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

@router.patch("/{id}", response_model=order_schema.OrderShow)
def update_order(id: int, order_data: order_schema.OrderUpdate,
                 session: Session = Depends(get_session),
                 current_user: User = Depends(get_current_user)):
    order = session.scalar(
        select(Order).where(Order.id == id, Order.user_id == current_user.id)
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.sqlmodel_update(order_data.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(order)

    return order

@router.delete("/{id}")
def delete_order(id: int, session: Session = Depends(get_session),
                 current_user: User = Depends(get_current_user)):
    order = session.scalar(
        select(Order).where(Order.id == id, Order.user_id == current_user.id)
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(order)
    session.commit()
