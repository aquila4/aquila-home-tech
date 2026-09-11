"""
app/__init__.py – Application factory.
Registers extensions, blueprints, error handlers and seeds the DB.
"""
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from config import config_map

# ── Extension instances (unbound until init_app) ─────────────────────────────
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(env: str = None) -> Flask:
    """Create and configure the Flask application."""

    env = env or os.environ.get("FLASK_ENV", "default")
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_map[env])

    # Ensure the instance and upload folders exist
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ── Bind extensions ───────────────────────────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "admin.login"
    login_manager.login_message = "Please log in to access the admin panel."
    login_manager.login_message_category = "warning"

    # ── Register blueprints ───────────────────────────────────────────────────
    from app.blueprints.main import main_bp
    from app.blueprints.products import products_bp
    from app.blueprints.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # ── Context processors ────────────────────────────────────────────────────
    @app.context_processor
    def inject_globals():
        from app.models import Category
        categories = Category.query.order_by(Category.name).all()
        return {
            "categories": categories,
            "whatsapp_number": app.config["WHATSAPP_NUMBER"],
            "business_phone": app.config["BUSINESS_PHONE"],
            "business_email": app.config["BUSINESS_EMAIL"],
            "business_address": app.config["BUSINESS_ADDRESS"],
        }

    # ── Error handlers ────────────────────────────────────────────────────────
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    # ── DB init + seed ────────────────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        _seed_db(app)

    return app


def _seed_db(app: Flask):
    """Seed the database with default categories and an admin user."""
    from app.models import Category, AdminUser

    default_categories = [
        ("Smart TVs", "smart-tvs", "📺"),
        ("Home Theaters", "home-theaters", "🎬"),
        ("Speakers", "speakers", "🔊"),
        ("Fridges", "fridges", "🧊"),
        ("Freezers", "freezers", "❄️"),
        ("Standing Fans", "standing-fans", "💨"),
        ("Ceiling Fans", "ceiling-fans", "🌀"),
        ("Stabilizers", "stabilizers", "⚡"),
        ("Electrical Accessories", "electrical-accessories", "🔌"),
        ("LED Bulbs", "led-bulbs", "💡"),
        ("Extension Boxes", "extension-boxes", "🔋"),
        ("Switches & Sockets", "switches-sockets", "🪛"),
    ]

    for name, slug, icon in default_categories:
        if not Category.query.filter_by(slug=slug).first():
            db.session.add(Category(name=name, slug=slug, icon=icon))

    if not AdminUser.query.filter_by(username=app.config["ADMIN_USERNAME"]).first():
        admin = AdminUser(
            username=app.config["ADMIN_USERNAME"],
            email=app.config["ADMIN_EMAIL"],
        )
        admin.set_password(app.config["ADMIN_PASSWORD"])
        db.session.add(admin)

    db.session.commit()
