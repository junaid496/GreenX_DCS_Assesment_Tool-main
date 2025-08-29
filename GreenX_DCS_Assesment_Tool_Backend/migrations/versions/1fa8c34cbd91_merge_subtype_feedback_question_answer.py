"""merge subtype, feedback, question_answer

Revision ID: 1fa8c34cbd91
Revises: 691a67563d0b, e06bd9a9ed13, 362df1345cbe
Create Date: 2025-07-05 07:59:31.692416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fa8c34cbd91'
down_revision = ('691a67563d0b', 'e06bd9a9ed13', '362df1345cbe')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
