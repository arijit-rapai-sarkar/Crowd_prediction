# backend/app/__init__.py

"""
App package initializer.

This allows the 'app' folder to be treated as a package,
so modules can be imported like `from app import models`.
"""

from .config import settings
from .database import Base, engine, SessionLocal

# Import models to ensure they are registered with SQLAlchemy's Base
from . import models

__all__ = [
    "settings",
    "Base",
    "engine",
    "SessionLocal",
    "models",
]
