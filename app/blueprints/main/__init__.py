"""
app/blueprints/main/__init__.py – Public-facing pages.
Routes: home, about, contact.
"""
from flask import Blueprint

main_bp = Blueprint("main", __name__, template_folder="../../templates")

from app.blueprints.main import routes  # noqa: E402, F401
