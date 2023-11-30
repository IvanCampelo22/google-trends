"""Model de Graficos do Google Trends

Revision ID: c20dcfb8069b
Revises: 
Create Date: 2023-11-28 19:07:39.978690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c20dcfb8069b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Graphic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('hour', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='google_trends'
    )
    op.create_index(op.f('ix_google_trends_Graphic_id'), 'Graphic', ['id'], unique=False, schema='google_trends')


def downgrade() -> None:
   pass