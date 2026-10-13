"""
Application Configuration.
Supports both MySQL 8.x (InnoDB transactional) and SQLite local development fallback.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'railway-dbms-secret-key-2026-secure')
    
    # Primary target is MySQL 8.x. Default falls back to SQLite file if MYSQL_DATABASE_URL not set
    # Example MySQL URL: mysql+pymysql://root:password@localhost:3306/railway_db
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        f"sqlite:///{BASE_DIR / 'railway.db'}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', 'False').lower() in ('true', '1')
    
    # Engine options for transactions and pool
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
    }


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
