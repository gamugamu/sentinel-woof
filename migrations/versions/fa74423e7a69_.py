"""empty message

Revision ID: fa74423e7a69
Revises: 2cde54cae8fd
Create Date: 2018-04-19 14:54:36.496910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa74423e7a69'
down_revision = '2cde54cae8fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('friends', sa.Column('status', sa.Integer(), nullable=True))
    op.drop_column('friends', 'extra_field')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('friends', sa.Column('extra_field', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('friends', 'status')
    # ### end Alembic commands ###
