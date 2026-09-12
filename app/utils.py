"""
app/utils.py – Shared utility functions.
Uses Cloudinary for image storage so images persist across Railway deploys.
"""
import os
import cloudinary
import cloudinary.uploader
from flask import current_app


# ── Configure Cloudinary ─────────────────────────────────────────────────────
cloudinary.config(
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME", "do8npxymr"),
    api_key    = os.environ.get("CLOUDINARY_API_KEY",    "478287198411895"),
    api_secret = os.environ.get("CLOUDINARY_API_SECRET", "mbNy9qwEbrzg76lCNlCqdhojXPE"),
    secure     = True,
)


def save_product_image(file_storage) -> str:
    """
    Upload a product image to Cloudinary.
    Returns the Cloudinary public URL to store in the DB.
    """
    try:
        # Upload to Cloudinary under 'aquila_home_tech/products' folder
        result = cloudinary.uploader.upload(
            file_storage,
            folder        = "aquila_home_tech/products",
            transformation = [
                {"width": 800, "height": 800, "crop": "limit"},
                {"quality": "auto"},
                {"fetch_format": "auto"},
            ],
        )
        # Return the secure URL
        return result["secure_url"]

    except Exception as e:
        current_app.logger.error(f"Cloudinary upload error: {e}")
        return "default_product.jpg"


def delete_product_image(image_url: str):
    """
    Delete a product image from Cloudinary using its URL.
    Skip default image or non-Cloudinary URLs.
    """
    if not image_url or image_url == "default_product.jpg":
        return
    if "cloudinary.com" not in image_url:
        return

    try:
        # Extract public_id from URL
        # URL format: https://res.cloudinary.com/cloud/image/upload/v123/folder/filename.ext
        parts      = image_url.split("/upload/")
        if len(parts) < 2:
            return
        public_id  = parts[1].rsplit(".", 1)[0]  # remove file extension
        # Remove version prefix if present (v1234567890/)
        if public_id.startswith("v") and "/" in public_id:
            public_id = "/".join(public_id.split("/")[1:])
        cloudinary.uploader.destroy(public_id)

    except Exception as e:
        current_app.logger.error(f"Cloudinary delete error: {e}")


def format_naira(value) -> str:
    """Format a number as Nigerian Naira."""
    try:
        return f"₦{float(value):,.2f}"
    except (TypeError, ValueError):
        return "₦0.00"