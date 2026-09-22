"""users create password

Revision ID: 534103f3a5c0
Revises: 1fde37c7465d
Create Date: 2026-09-11 13:22:21.328316

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '534103f3a5c0'
down_revision: Union[str, Sequence[str], None] = '1fde37c7465d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('password', sa.String(100), nullable=False))

def downgrade() -> None:
    op.drop_column("users", "password")
