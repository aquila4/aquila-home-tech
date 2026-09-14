"""
app/utils.py - Image upload via Cloudinary.
Images are stored permanently in the cloud - never lost on Railway redeploy.
"""
import os
import cloudinary
import cloudinary.uploader
from flask import current_app

# Configure Cloudinary
cloudinary.config(
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME", "do8npxymr"),
    api_key    = os.environ.get("CLOUDINARY_API_KEY",    "478287198411895"),
    api_secret = os.environ.get("CLOUDINARY_API_SECRET", "mbNy9qwEbrzg76lCNlCqdhojXPE"),
    secure     = True,
)


def save_product_image(file_storage) -> str:
    """
    Upload image to Cloudinary.
    Returns the full Cloudinary URL (https://res.cloudinary.com/...)
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
        # Return full secure URL - this is what gets saved to database
        return result["secure_url"]

    except Exception as e:
        if current_app:
            current_app.logger.error(f"Cloudinary upload error: {e}")
        print(f"Cloudinary upload error: {e}")
        return "default_product.jpg"


def delete_product_image(image_url: str):
    """
    Delete image from Cloudinary using its URL.
    Skips default image and non-Cloudinary URLs.
    """
    if not image_url:
        return
    if image_url == "default_product.jpg":
        return
    if "cloudinary.com" not in str(image_url):
        return

    try:
        # Extract public_id from Cloudinary URL
        # URL: https://res.cloudinary.com/cloud/image/upload/v123/folder/file.jpg
        parts = image_url.split("/upload/")
        if len(parts) < 2:
            return
        # Remove version (v1234/) and extension
        after_upload = parts[1]
        if after_upload.startswith("v") and "/" in after_upload:
            after_upload = "/".join(after_upload.split("/")[1:])
        public_id = after_upload.rsplit(".", 1)[0]
        cloudinary.uploader.destroy(public_id)

    except Exception as e:
        if current_app:
            current_app.logger.error(f"Cloudinary delete error: {e}")
        print(f"Cloudinary delete error: {e}")


def format_naira(value) -> str:
    """Format number as Nigerian Naira."""
    try:
        return f"₦{float(value):,.2f}"
    except (TypeError, ValueError):
        return "₦0.00"