"""create model for related_entities

Revision ID: 69c3759b614e
Revises: b247097e0266
Create Date: 2023-12-18 16:47:37.584763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69c3759b614e'
down_revision: Union[str, None] = 'b247097e0266'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('RelatedEtities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('param', sa.String(), nullable=True),
    sa.Column('initial_date', sa.String(), nullable=True),
    sa.Column('end_date', sa.String(), nullable=True),
    sa.Column('entities', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_RelatedEtities_id'), 'RelatedEtities', ['id'], unique=False)

def downgrade() -> None:
    pass
