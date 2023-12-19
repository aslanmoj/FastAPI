"""Create Post Table

Revision ID: 5b32238ecafe
Revises: 
Create Date: 2023-12-18 16:17:56.523223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b32238ecafe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(): 
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer,nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        
    )


def downgrade() :
    op.drop_table('posts')
