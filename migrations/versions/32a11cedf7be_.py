"""empty message

Revision ID: 32a11cedf7be
Revises: 61f07127a7c4
Create Date: 2020-09-22 05:44:51.200057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32a11cedf7be'
down_revision = '61f07127a7c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cars', sa.Column('status', sa.String(length=20), nullable=True))
    op.create_unique_constraint(None, 'history', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'history', type_='unique')
    op.drop_column('cars', 'status')
    # ### end Alembic commands ###
