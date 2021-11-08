"""Initial Migration

Revision ID: 542fe9a9b0fa
Revises: bcec1b7bc93f
Create Date: 2021-11-07 19:20:26.483595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '542fe9a9b0fa'
down_revision = 'bcec1b7bc93f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile_photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pic_path', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profile_photos')
    # ### end Alembic commands ###