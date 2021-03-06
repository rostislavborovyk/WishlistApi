"""init migration

Revision ID: e782f22dd36a
Revises: 
Create Date: 2020-09-05 11:29:28.502907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e782f22dd36a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wishlists',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('add_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_wishlist_association',
    sa.Column('user_id', sa.String(length=32), nullable=False),
    sa.Column('wishlist_id', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['wishlist_id'], ['wishlists.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'wishlist_id')
    )
    op.create_table('wishlist_items',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('text', sa.String(length=200), nullable=True),
    sa.Column('is_reserved', sa.Boolean(), nullable=True),
    sa.Column('wishlist_id', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['wishlist_id'], ['wishlists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wishlist_items')
    op.drop_table('user_wishlist_association')
    op.drop_table('wishlists')
    op.drop_table('users')
    # ### end Alembic commands ###
