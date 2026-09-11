"""
generate_placeholder.py – Creates a default product image.
Run once: python generate_placeholder.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_default_image():
    img = Image.new('RGB', (400, 400), color='#F0F2F5')
    draw = ImageDraw.Draw(img)

    # Draw a simple icon placeholder
    draw.rectangle([140, 120, 260, 240], outline='#9BA4B5', width=3)
    draw.ellipse([165, 135, 195, 165], fill='#9BA4B5')
    draw.polygon([(140, 240), (180, 180), (220, 210), (260, 150), (260, 240)], fill='#C5CDD8')

    # Text
    draw.text((200, 270), "No Image", fill='#9BA4B5', anchor='mm')
    draw.text((200, 295), "Available", fill='#9BA4B5', anchor='mm')

    os.makedirs('app/static/images/uploads', exist_ok=True)
    img.save('app/static/images/default_product.jpg', quality=85)
    print("✓ Default product image created.")

if __name__ == '__main__':
    create_default_image()
