"""
app/utils.py - Image upload via Cloudinary.
Credentials loaded from environment variables only - never hardcoded.
"""
import os
import cloudinary
import cloudinary.uploader
from flask import current_app

# Configure Cloudinary from environment variables only
cloudinary.config(
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key    = os.environ.get("CLOUDINARY_API_KEY"),
    api_secret = os.environ.get("CLOUDINARY_API_SECRET"),
    secure     = True,
)


def save_product_image(file_storage) -> str:
    """
    Upload image to Cloudinary.
    Returns the full Cloudinary URL to store in the database.
    """
    try:
        result = cloudinary.uploader.upload(
            file_storage,
            folder="aquila_home_tech/products",
            transformation=[
                {"width": 800, "height": 800, "crop": "limit"},
                {"quality": "auto"},
                {"fetch_format": "auto"},
            ],
        )
        return result["secure_url"]

    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return "default_product.jpg"


def delete_product_image(image_url: str):
    """
    Delete image from Cloudinary.
    Skips default image and non-Cloudinary URLs.
    """
    if not image_url:
        return
    if image_url == "default_product.jpg":
        return
    if "cloudinary.com" not in str(image_url):
        return

    try:
        # Extract public_id from URL
        parts = image_url.split("/upload/")
        if len(parts) < 2:
            return
        after_upload = parts[1]
        if after_upload.startswith("v") and "/" in after_upload:
            after_upload = "/".join(after_upload.split("/")[1:])
        public_id = after_upload.rsplit(".", 1)[0]
        cloudinary.uploader.destroy(public_id)

    except Exception as e:
        print(f"Cloudinary delete error: {e}")


def format_naira(value) -> str:
    try:
        return f"₦{float(value):,.2f}"
    except (TypeError, ValueError):
        return "₦0.00"