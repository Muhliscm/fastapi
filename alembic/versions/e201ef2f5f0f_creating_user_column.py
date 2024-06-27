"""creating user column

Revision ID: e201ef2f5f0f
Revises: 85c6e8693234
Create Date: 2024-06-27 11:33:09.606722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e201ef2f5f0f'
down_revision: Union[str, None] = '85c6e8693234'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id',
                                       sa.Integer, nullable=False),
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    op.drop_table('posts')
