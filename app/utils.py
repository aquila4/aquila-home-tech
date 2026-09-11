"""
app/utils.py – Shared utility functions.
"""
import os
import uuid
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_product_image(file_storage) -> str:
    """
    Resize and save an uploaded product image.
    Returns the filename string to store in the DB.
    """
    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    save_path = os.path.join(upload_folder, unique_name)

    # Resize to max 800×800 while preserving aspect ratio
    img = Image.open(file_storage)
    img = img.convert("RGB")
    img.thumbnail((800, 800), Image.LANCZOS)
    img.save(save_path, optimize=True, quality=85)

    return unique_name


def delete_product_image(filename: str):
    """Remove a product image from disk (skip default image)."""
    if not filename or filename == "default_product.jpg":
        return
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(path):
        os.remove(path)


def format_naira(value) -> str:
    """Format a number as Nigerian Naira."""
    try:
        return f"₦{float(value):,.2f}"
    except (TypeError, ValueError):
        return "₦0.00"
