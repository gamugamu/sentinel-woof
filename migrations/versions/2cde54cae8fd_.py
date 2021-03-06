"""empty message

Revision ID: 2cde54cae8fd
Revises: 98ab210b67a1
Create Date: 2018-04-19 11:23:19.171211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cde54cae8fd'
down_revision = '98ab210b67a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('friends', sa.Column('user_from', sa.Integer(), nullable=False))
    op.add_column('friends', sa.Column('user_to', sa.Integer(), nullable=False))
    op.drop_constraint(u'friends_myfriend_id_fkey', 'friends', type_='foreignkey')
    op.drop_constraint(u'friends_friend_id_fkey', 'friends', type_='foreignkey')
    op.create_foreign_key(None, 'friends', 'petsowner', ['user_from'], ['id'])
    op.create_foreign_key(None, 'friends', 'petsowner', ['user_to'], ['id'])
    op.drop_column('friends', 'friend_id')
    op.drop_column('friends', 'myfriend_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('friends', sa.Column('myfriend_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('friends', sa.Column('friend_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'friends', type_='foreignkey')
    op.drop_constraint(None, 'friends', type_='foreignkey')
    op.create_foreign_key(u'friends_friend_id_fkey', 'friends', 'petsowner', ['friend_id'], ['id'])
    op.create_foreign_key(u'friends_myfriend_id_fkey', 'friends', 'petsowner', ['myfriend_id'], ['id'])
    op.drop_column('friends', 'user_to')
    op.drop_column('friends', 'user_from')
    # ### end Alembic commands ###
