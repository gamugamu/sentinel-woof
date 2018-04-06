"""empty message

Revision ID: f186f475d05c
Revises: 41b7ba29d568
Create Date: 2018-04-06 17:07:24.107922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f186f475d05c'
down_revision = '41b7ba29d568'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('petsowner')
    op.drop_table('pet')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pet',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('woof_name', sa.VARCHAR(length=41), autoincrement=False, nullable=True),
    sa.Column('parent_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], [u'petsowner.id'], name=u'pet_parent_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'pet_pkey')
    )
    op.create_table('petsowner',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('sentinel_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('mail', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('seed', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'petsowner_pkey')
    )
    # ### end Alembic commands ###
