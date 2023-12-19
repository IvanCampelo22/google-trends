"""add region in RelatedEntities

Revision ID: d1bf1429a3da
Revises: 0720ad26563f
Create Date: 2023-12-18 21:58:56.894159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1bf1429a3da'
down_revision: Union[str, None] = '0720ad26563f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('RelatedEtities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('param', sa.String(), nullable=True),
    sa.Column('initial_date', sa.String(), nullable=True),
    sa.Column('end_date', sa.String(), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('entities', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid'),
    schema='google_trends'
    )
    op.create_index(op.f('ix_google_trends_RelatedEtities_id'), 'RelatedEtities', ['id'], unique=False, schema='google_trends')


def downgrade() -> None:
    pass
