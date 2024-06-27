"""creating_content_coulumn

Revision ID: 85c6e8693234
Revises: 06b9f52ebb73
Create Date: 2024-06-27 11:25:44.900725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85c6e8693234'
down_revision: Union[str, None] = '06b9f52ebb73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
