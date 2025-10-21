"""Merge multiple heads

Revision ID: 6c65e8a3b0b2
Revises: 2af17d5b7d36, 729637185d87
Create Date: 2025-10-21 13:04:30.927585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c65e8a3b0b2'
down_revision: Union[str, None] = ('2af17d5b7d36', '729637185d87')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
