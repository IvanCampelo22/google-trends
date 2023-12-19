"""RelatedEntitiesRising

Revision ID: 2597b60db609
Revises: d1bf1429a3da
Create Date: 2023-12-19 15:14:23.491078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2597b60db609'
down_revision: Union[str, None] = 'd1bf1429a3da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('RelatedEtitiesRising',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('param', sa.String(), nullable=True),
    sa.Column('initial_date', sa.String(), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('end_date', sa.String(), nullable=True),
    sa.Column('entities', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid'),
    schema='google_trends'
    )
    op.create_index(op.f('ix_google_trends_RelatedEtitiesRising_id'), 'RelatedEtitiesRising', ['id'], unique=False, schema='google_trends')
    op.create_table('RelatedEtitiesTop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('param', sa.String(), nullable=True),
    sa.Column('initial_date', sa.String(), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('end_date', sa.String(), nullable=True),
    sa.Column('entities', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid'),
    schema='google_trends'
    )
    op.create_index(op.f('ix_google_trends_RelatedEtitiesTop_id'), 'RelatedEtitiesTop', ['id'], unique=False, schema='google_trends')
    

def downgrade() -> None:
    pass