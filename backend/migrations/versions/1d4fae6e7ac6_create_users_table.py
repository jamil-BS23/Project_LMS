"""create users table

Revision ID: 1d4fae6e7ac6
Revises: 9c1cc49b7759
Create Date: 2025-10-20 18:11:49.522474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d4fae6e7ac6'
down_revision: Union[str, None] = '9c1cc49b7759'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
