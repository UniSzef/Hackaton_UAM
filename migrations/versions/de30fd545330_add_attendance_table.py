"""Add attendance table

Revision ID: de30fd545330
Revises: 2e8be295db25
Create Date: 2024-06-16 00:34:21.317956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de30fd545330'
down_revision = '2e8be295db25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attendance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('present', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attendance')
    # ### end Alembic commands ###