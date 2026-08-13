# --- DNK-MRH-HEADER ---
# mrh_id: "services/dnk_canvas_api/alembic/versions/agent_timeline_001_timeline_table.py"
# purpose: "Create agent_timeline table for observability and tracking agent actions"
# author: "DNK-e.com Maksym"
# license: "MIT"
# canonical_source: true
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-13"
# --- END DNK-MRH-HEADER ---

"""Create agent_timeline table

Revision ID: agent_timeline_001
Revises: security_gates_001  # Остання ревізія з Security Gates
Create Date: 2026-08-13

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'agent_timeline_001'
down_revision = 'security_gates_001'  # Посилаємось на Security Gates
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'agent_timeline',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('run_id', sa.UUID(), nullable=False),
        sa.Column('agent_id', sa.String(255), nullable=False),
        sa.Column('event_type', sa.String(50), nullable=False),  # action_start, action_end, error
        sa.Column('status', sa.String(50), nullable=True),  # pending, success, failed
        sa.Column('action_name', sa.String(255), nullable=False),
        sa.Column('payload_json', postgresql.JSONB(), nullable=True),
        sa.Column('idempotency_key', sa.String(64), nullable=True),
        sa.Column('timestamp', sa.TIMESTAMP(), server_default=sa.func.now()),
    )
    
    # Індекси для швидкого пошуку
    op.create_index('idx_timeline_run', 'agent_timeline', ['run_id'])
    op.create_index('idx_timeline_agent', 'agent_timeline', ['agent_id'])
    op.create_index('idx_timeline_timestamp', 'agent_timeline', ['timestamp'])
    op.create_index('idx_timeline_idempotency', 'agent_timeline', ['idempotency_key'])


def downgrade():
    op.drop_index('idx_timeline_idempotency', table_name='agent_timeline')
    op.drop_index('idx_timeline_timestamp', table_name='agent_timeline')
    op.drop_index('idx_timeline_agent', table_name='agent_timeline')
    op.drop_index('idx_timeline_run', table_name='agent_timeline')
    op.drop_table('agent_timeline')
