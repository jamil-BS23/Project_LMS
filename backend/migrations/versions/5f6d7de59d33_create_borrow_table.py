"""create borrow table

Revision ID: 5f6d7de59d33
Revises: 
Create Date: 2025-10-20 17:49:10.651422

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f6d7de59d33'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5f6d7de59d33'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'borrow',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('book_id', sa.Integer, sa.ForeignKey('books.id')),
        sa.Column('borrower_name', sa.String(100), nullable=False),
        sa.Column('borrow_date', sa.Date, nullable=False),
        sa.Column('return_date', sa.Date, nullable=True),
    )

def downgrade():
    op.drop_table('borrow')
