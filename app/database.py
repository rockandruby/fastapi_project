from sqlmodel import Session, create_engine
from .settings import DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

def get_session():
    with Session(engine) as session:
        yield session
