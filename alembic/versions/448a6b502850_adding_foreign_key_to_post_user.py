"""adding foreign key to post user

Revision ID: 448a6b502850
Revises: e201ef2f5f0f
Create Date: 2024-06-27 14:01:44.380856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '448a6b502850'
down_revision: Union[str, None] = 'e201ef2f5f0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_user_fkey', source_table='posts',
                          referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_user_fkey', 'posts')
