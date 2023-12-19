"""add foreign key

Revision ID: 88024a2addf6
Revises: 23dfe6ebd61a
Create Date: 2023-12-18 16:47:44.815398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88024a2addf6'
down_revision: Union[str, None] = '23dfe6ebd61a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete= "CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_user_fk', table_name= 'posts')
    op.drop_column('posts', 'owner_id')
    pass
