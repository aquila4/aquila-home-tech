"""
app/blueprints/products/__init__.py – Product catalogue blueprint.
"""
from flask import Blueprint

products_bp = Blueprint("products", __name__, template_folder="../../templates")

from app.blueprints.products import routes  # noqa: E402, F401
