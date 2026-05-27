import os
import sys

# Add the 'backend' directory to sys.path so alembic can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
