"""add_published_at_revised_at_fields

Revision ID: 18_a8cd0dc08805
Revises: 17_424e875043d3
Create Date: 2021-09-16 13:41:09.534116

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "18_a8cd0dc08805"
down_revision = "17_424e875043d3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("dataset", sa.Column("published_at", sa.DateTime(), nullable=True))
    op.add_column("dataset", sa.Column("revised_at", sa.DateTime(), nullable=True))
    op.add_column("project", sa.Column("published_at", sa.DateTime(), nullable=True))
    op.add_column("project", sa.Column("revised_at", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("project", "revised_at")
    op.drop_column("project", "published_at")
    op.drop_column("dataset", "revised_at")
    op.drop_column("dataset", "published_at")
    # ### end Alembic commands ###
