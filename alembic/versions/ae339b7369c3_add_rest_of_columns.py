"""add rest of columns

Revision ID: ae339b7369c3
Revises: 88024a2addf6
Create Date: 2023-12-18 16:56:50.679221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae339b7369c3'
down_revision: Union[str, None] = '88024a2addf6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(),nullable=False, server_default='True')
    )
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('NOW()'))
    )


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
