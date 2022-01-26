"""comment model

Revision ID: acbbef2e5b53
Revises: 81e0fe67e6db
Create Date: 2022-01-25 23:01:26.520832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acbbef2e5b53'
down_revision = '81e0fe67e6db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['image.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###
