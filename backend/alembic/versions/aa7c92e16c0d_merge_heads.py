"""Merge heads

Revision ID: aa7c92e16c0d
Revises: 2af17d5b7d36, 729637185d87
Create Date: 2025-10-20 20:19:50.254980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa7c92e16c0d'
down_revision: Union[str, None] = ('2af17d5b7d36', '729637185d87')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
