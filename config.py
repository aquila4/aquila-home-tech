"""
config.py – Application configuration classes.
Switch between environments by setting FLASK_ENV in .env.
"""
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration shared across all environments."""

    # ── Security ────────────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback-secret-change-me")

    # ── Database ────────────────────────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'aquila.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── File uploads ────────────────────────────────────────────────────────
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR, os.environ.get("UPLOAD_FOLDER", "app/static/images/uploads")
    )
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    # ── Business meta ────────────────────────────────────────────────────────
    WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "2348105208988")
    BUSINESS_PHONE = os.environ.get("BUSINESS_PHONE", "+234 704 792 7308")
    BUSINESS_EMAIL = os.environ.get("BUSINESS_EMAIL", "info@aquilahometech.com")
    BUSINESS_ADDRESS = os.environ.get(
        "BUSINESS_ADDRESS", "12 Electronics Road, GRA, Ilorin, Kwara State, Nigeria"
    )

    # ── Admin seed ───────────────────────────────────────────────────────────
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@aquilahometech.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin@1234!")

    # ── Pagination ───────────────────────────────────────────────────────────
    PRODUCTS_PER_PAGE = 12


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # Enforce HTTPS redirects when behind a reverse proxy
    PREFERRED_URL_SCHEME = "https"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
