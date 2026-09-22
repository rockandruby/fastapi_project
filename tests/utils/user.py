from app.models.user import User

def create_user(session, data: dict | None = None) -> User:
    if not data:
        user = User(name="John", email="foo@example.com", password="123")
    else:
        user = User(**data)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
