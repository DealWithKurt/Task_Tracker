import pytest
from app.models.task import Task
from app.models.user import User

def test_transaction_rollback(db):
    """Test that a transaction rollback discards changes"""
    # Create a user in this transaction
    user = User(name="Rollback Test", email="rollback@example.com", role="user", hashed_password="pw")
    db.add(user)
    db.flush()
    
    # We rollback explicitly to simulate a failure
    db.rollback()
    
    # Verify it doesn't exist in the current session
    check = db.query(User).filter(User.email == "rollback@example.com").first()
    assert check is None
