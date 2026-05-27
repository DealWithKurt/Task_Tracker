from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.migration import MigrationContext
from app.database import engine
from sqlalchemy import text


def test_migration_history():
    """Test that alembic migration history is available and contains our revision"""
    alembic_cfg = Config("alembic.ini")
    script = ScriptDirectory.from_config(alembic_cfg)

    heads = script.get_heads()
    assert len(heads) >= 1, "At least one migration head should exist"

    # Get current revision from database
    with engine.connect() as conn:
        context = MigrationContext.configure(conn)
        current_rev = context.get_current_revision()

    # Current revision should be one of the heads
    assert current_rev in heads, f"Current revision {current_rev} should be in heads {heads}"


def test_migration_head_revision():
    """Test that migration head is 'add tables' revision"""
    alembic_cfg = Config("alembic.ini")
    script = ScriptDirectory.from_config(alembic_cfg)

    heads = script.get_heads()
    assert len(heads) == 1, "Should have exactly one head"
    assert heads[0] == "0c26951198da", f"Head should be 0c26951198da, got {heads[0]}"


def test_tables_exist():
    """Test that expected database tables exist after migrations"""
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public' ORDER BY table_name"
            )
        )
        tables = [row[0] for row in result]

    assert "users" in tables, "users table should exist"
    assert "tasks" in tables, "tasks table should exist"
    assert "comments" in tables, "comments table should exist"