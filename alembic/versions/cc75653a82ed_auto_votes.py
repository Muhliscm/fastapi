"""auto-votes

Revision ID: cc75653a82ed
Revises: bf4b988e4c41
Create Date: 2024-06-27 15:23:56.819822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc75653a82ed'
down_revision: Union[str, None] = 'bf4b988e4c41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('title', sa.String(), nullable=False))
    op.drop_column('posts', 'post')
    op.create_foreign_key(None, 'votes', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'votes', type_='foreignkey')
    op.add_column('posts', sa.Column('post', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('posts', 'title')
    # ### end Alembic commands ###