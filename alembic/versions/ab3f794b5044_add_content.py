"""Add Content

Revision ID: ab3f794b5044
Revises: 5b32238ecafe
Create Date: 2023-12-18 16:35:33.312175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab3f794b5044'
down_revision: Union[str, None] = '5b32238ecafe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
