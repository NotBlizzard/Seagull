"""create images table

Revision ID: 4dadbcde16dd
Revises: 8401fe68374e
Create Date: 2020-03-11 22:29:44.584404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dadbcde16dd'
down_revision = '8401fe68374e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
      'images',
      sa.Column('id', sa.Integer, primary_key=True),
      sa.Column('image_path', sa.String),
      sa.Column('user_id', sa.Integer),
    )



def downgrade():
    op.drop_table('images')
