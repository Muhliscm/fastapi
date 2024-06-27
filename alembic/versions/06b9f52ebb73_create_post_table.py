"""create_post_table

Revision ID: 06b9f52ebb73
Revises: 
Create Date: 2024-06-27 10:44:30.723736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06b9f52ebb73'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column(
        'id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('post', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
