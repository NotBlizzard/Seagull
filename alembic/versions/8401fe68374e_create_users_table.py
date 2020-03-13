"""create users table

Revision ID: 8401fe68374e
Revises:
Create Date: 2020-03-11 02:03:25.583779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8401fe68374e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
      'users',
      sa.Column('id', sa.Integer, primary_key=True),
      sa.Column('username', sa.String),
      sa.Column('password', sa.String, nullable=True),
      sa.Column('email', sa.String, nullable=True),
      sa.Column('githubId', sa.Integer, nullable=True),
      sa.Column('googleId', sa.Integer, nullable=True)
    )


def downgrade():
    op.drop_table('users')
