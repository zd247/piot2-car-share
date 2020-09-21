"""empty message

Revision ID: decfaacb9590
Revises: 32a11cedf7be
Create Date: 2020-09-22 05:51:07.421471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'decfaacb9590'
down_revision = '32a11cedf7be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cars', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cars', sa.Column('status', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
