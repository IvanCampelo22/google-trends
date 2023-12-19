"""RelatedQueriesRising

Revision ID: 3565fa369225
Revises: 2597b60db609
Create Date: 2023-12-19 16:36:12.120794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3565fa369225'
down_revision: Union[str, None] = '2597b60db609'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table('RelatedQueriesRising',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('param', sa.String(), nullable=True),
    sa.Column('initial_date', sa.String(), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('end_date', sa.String(), nullable=True),
    sa.Column('queries', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid'),
    schema='google_trends'
    )
    op.create_index(op.f('ix_google_trends_RelatedQueriesRising_id'), 'RelatedQueriesRising', ['id'], unique=False, schema='google_trends')
    op.create_table('RelatedQueriesTop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('param', sa.String(), nullable=True),
    sa.Column('initial_date', sa.String(), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('end_date', sa.String(), nullable=True),
    sa.Column('queries', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid'),
    schema='google_trends'
    )
    op.create_index(op.f('ix_google_trends_RelatedQueriesTop_id'), 'RelatedQueriesTop', ['id'], unique=False, schema='google_trends')


def downgrade() -> None:
    pass
