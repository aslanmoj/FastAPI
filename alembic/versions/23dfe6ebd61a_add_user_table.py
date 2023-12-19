"""add user table

Revision ID: 23dfe6ebd61a
Revises: ab3f794b5044
Create Date: 2023-12-18 16:40:25.310365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23dfe6ebd61a'
down_revision: Union[str, None] = 'ab3f794b5044'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
        op.create_table(
        'users',
        sa.Column('id', sa.Integer(),nullable=False),
        sa.Column('email', sa.String(),nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True)
                  ,server_default=sa.text('now()'),nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        
    )


def downgrade():
    op.drop_table('users')
    pass
