"""adding remaining columns to post table

Revision ID: bf4b988e4c41
Revises: 448a6b502850
Create Date: 2024-06-27 14:31:13.739627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf4b988e4c41'
down_revision: Union[str, None] = '448a6b502850'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('posts', sa.Column('published', sa.Boolean,
                  server_default=sa.text('TRUE'), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
