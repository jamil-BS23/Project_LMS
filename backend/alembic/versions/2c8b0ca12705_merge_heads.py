"""Merge heads

Revision ID: 2c8b0ca12705
Revises: 2987bc8160a7, cbeb3312b7c2
Create Date: 2025-10-22 15:01:33.719875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c8b0ca12705'
down_revision: Union[str, None] = ('2987bc8160a7', 'cbeb3312b7c2')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
