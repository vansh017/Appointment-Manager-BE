"""Initial Migration Added

Revision ID: cf1eeec1c208
Revises: d69136e16fe2
Create Date: 2024-12-23 18:31:36.226176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'cf1eeec1c208'
down_revision: Union[str, None] = 'd69136e16fe2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bearer_token',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('access_token', mysql.LONGTEXT(), nullable=False),
    sa.Column('refresh_token', sa.VARCHAR(length=255), nullable=True),
    sa.Column('expires_on', sa.DateTime(), nullable=False),
    sa.Column('is_revoked', sa.Boolean(), nullable=False),
    sa.Column('state', sa.VARCHAR(length=255), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_token'),
    sa.UniqueConstraint('refresh_token')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bearer_token')
    # ### end Alembic commands ###
