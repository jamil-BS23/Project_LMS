"""create users table

Revision ID: 9c1cc49b7759
Revises: 5f6d7de59d33
Create Date: 2025-10-20 18:09:46.897380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c1cc49b7759'
down_revision: Union[str, None] = '5f6d7de59d33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
