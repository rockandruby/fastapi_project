from app.models.order import Order

def create_order(session, user, data: dict | None = None) -> Order:
    if not data:
        order = Order(title="Test Order")
    else:
        order = Order(**data)
    order.user = user
    session.add(order)
    session.commit()
    session.refresh(order)

    return order
