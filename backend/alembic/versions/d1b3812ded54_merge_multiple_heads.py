"""Merge multiple heads

Revision ID: d1b3812ded54
Revises: 2987bc8160a7, cbeb3312b7c2
Create Date: 2025-11-04 13:17:10.422896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1b3812ded54'
down_revision: Union[str, None] = ('2987bc8160a7', 'cbeb3312b7c2')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
