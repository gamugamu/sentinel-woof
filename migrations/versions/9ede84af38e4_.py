"""empty message

Revision ID: 9ede84af38e4
Revises: 8bb6e0536358
Create Date: 2018-04-18 14:21:45.510844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ede84af38e4'
down_revision = '8bb6e0536358'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feed', sa.Column('_petowner_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('feed', '_petowner_id')
    # ### end Alembic commands ###
