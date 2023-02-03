"""harmonize_schema_state_prod

Revision ID: 06_9023d0bf61ab
Revises: 05_d9fb29897244
Create Date: 2020-08-28 15:00:56.262160

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "06_9023d0bf61ab"
down_revision = "05_d9fb29897244"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("dataset_deployment")
    op.alter_column("dataset", "project_id", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("dataset", "project_status", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("dataset", "revision", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("deployment_directory", "created_at", existing_type=postgresql.TIMESTAMP(), nullable=False)
    op.alter_column("deployment_directory", "dataset_id", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("deployment_directory", "updated_at", existing_type=postgresql.TIMESTAMP(), nullable=False)
    op.create_foreign_key(None, "deployment_directory", "dataset", ["dataset_id"], ["id"])
    op.alter_column("project", "needs_attestation", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column(
        "project",
        "processing_state",
        existing_type=postgresql.ENUM(
            "NA", "IN_VALIDATION", "IN_ARTIFACT_CREATION", "IN_DEPLOYMENT", name="processingstate"
        ),
        nullable=True,
    )
    op.alter_column(
        "project",
        "validation_state",
        existing_type=postgresql.ENUM("NOT_VALIDATED", "VALID", "INVALID", name="validationstate"),
        nullable=True,
    )
    # ### end Alembic commands ###


def downgrade():

    raise NotImplementedError(
        """Unfortunately, you cannot downgrade reliably from this point. The databases
         were out of sync with alembic and each other, and this is the revision that syncs them back
         up. If you want to downgrade, you're going to need to upgrade in a downward dirction."""
    )


#    # ### commands auto generated by Alembic - please adjust! ###
#    op.alter_column(
#        "project",
#        "validation_state",
#        existing_type=postgresql.ENUM("NOT_VALIDATED", "VALID", "INVALID", name="validationstate"),
#        nullable=False,
#    )
#    op.alter_column(
#        "project",
#        "processing_state",
#        existing_type=postgresql.ENUM(
#            "NA", "IN_VALIDATION", "IN_ARTIFACT_CREATION", "IN_DEPLOYMENT", name="processingstate"
#        ),
#        nullable=False,
#    )
#    op.alter_column("project", "needs_attestation", existing_type=sa.BOOLEAN(), nullable=False)
#    op.drop_constraint(None, "deployment_directory", type_="foreignkey")
#    op.alter_column("deployment_directory", "updated_at", existing_type=postgresql.TIMESTAMP(), nullable=True)
#    op.alter_column("deployment_directory", "dataset_id", existing_type=sa.VARCHAR(), nullable=True)
#    op.alter_column("deployment_directory", "created_at", existing_type=postgresql.TIMESTAMP(), nullable=True)
#    op.alter_column("dataset", "revision", existing_type=sa.INTEGER(), nullable=False)
#    op.alter_column("dataset", "project_status", existing_type=sa.VARCHAR(), nullable=True)
#    op.alter_column("dataset", "project_id", existing_type=sa.VARCHAR(), nullable=True)
#    op.create_table(
#        "dataset_deployment",
#        sa.Column("id", sa.VARCHAR(), autoincrement=False, nullable=False),
#        sa.Column("dataset_id", sa.VARCHAR(), autoincrement=False, nullable=False),
#        sa.Column("environment", sa.VARCHAR(), autoincrement=False, nullable=True),
#        sa.Column("url", sa.VARCHAR(), autoincrement=False, nullable=True),
#        sa.Column(
#            "created_at", postgresql.TIMESTAMP(), server_default=sa.text("now()"), autoincrement=False, nullable=False
#        ),
#        sa.Column(
#            "updated_at", postgresql.TIMESTAMP(), server_default=sa.text("now()"), autoincrement=False, nullable=False
#        ),
#        sa.ForeignKeyConstraint(["dataset_id"], ["dataset.id"], name="fk_dataset_id"),
#        sa.PrimaryKeyConstraint("id", name="dataset_deployment_pkey"),
#    )
#    # ### end Alembic commands ###
