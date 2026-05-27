import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import os

from app.main import app
from app.database import Base, get_db
from app.config import settings
import alembic.config
import alembic.command
from alembic.config import Config

# For tests, use the same database as it's required (with db test fixture)
# We can use a test database if preferred, but since there's no instruction to create a test DB, 
# we'll use a transaction rollback test strategy on the actual DB or use an isolated one.
# Given the instructions, we can just use the provided database but rollback changes.

engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    try:
        alembic_cfg = Config("alembic.ini")
        alembic.command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(f"Migration error: {e}")
    
    yield

@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture
def test_user(client, db):
    # Create test user
    import bcrypt
    from app.models.user import User
    
    def _get_password_hash(password):
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
    
    # Check if exists
    user = db.query(User).filter(User.email == "test@example.com").first()
    if not user:
        user = User(
            name="Test User",
            email="test@example.com",
            role="admin",
            hashed_password=_get_password_hash("testpass")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

@pytest.fixture
def auth_headers(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "testpass"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
