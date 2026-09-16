"""
app/models.py – SQLAlchemy ORM models.
Supports multiple product images and video from any platform.
"""
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class Category(db.Model):
    __tablename__ = "categories"
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False, unique=True)
    slug        = db.Column(db.String(120), nullable=False, unique=True, index=True)
    icon        = db.Column(db.String(10), default="🛒")
    description = db.Column(db.Text, default="")
    created_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    products    = db.relationship("Product", backref="category", lazy="dynamic")

    @property
    def product_count(self):
        return self.products.count()


class ProductImage(db.Model):
    __tablename__ = "product_images"
    id         = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    image_url  = db.Column(db.String(500), nullable=False)
    is_main    = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Product(db.Model):
    __tablename__ = "products"
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(200), nullable=False)
    slug           = db.Column(db.String(220), nullable=False, unique=True, index=True)
    category_id    = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    description    = db.Column(db.Text, default="")
    specifications = db.Column(db.Text, default="")
    price          = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    old_price      = db.Column(db.Numeric(12, 2), nullable=True)
    image          = db.Column(db.String(500), default="default_product.jpg")
    stock_quantity = db.Column(db.Integer, default=0)
    featured       = db.Column(db.Boolean, default=False, index=True)
    is_active      = db.Column(db.Boolean, default=True, index=True)
    video_url      = db.Column(db.String(500), nullable=True)
    video_platform = db.Column(db.String(20), nullable=True)
    created_at     = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at     = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    images = db.relationship("ProductImage", backref="product", lazy="dynamic",
                             cascade="all, delete-orphan", order_by="ProductImage.sort_order")

    @property
    def formatted_price(self):
        return f"₦{self.price:,.2f}"

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    @property
    def in_stock(self):
        return self.stock_quantity > 0

    @property
    def main_image(self):
        main = self.images.filter_by(is_main=True).first()
        if main:
            return main.image_url
        first = self.images.order_by(ProductImage.sort_order).first()
        if first:
            return first.image_url
        return self.image

    @property
    def all_images_list(self):
        return list(self.images.order_by(ProductImage.sort_order).all())

    @property
    def embed_video_url(self):
        if not self.video_url:
            return None
        url = self.video_url.strip()
        if "youtube.com/watch" in url:
            vid_id = url.split("v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{vid_id}"
        if "youtu.be/" in url:
            vid_id = url.split("youtu.be/")[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{vid_id}"
        if "facebook.com" in url or "fb.watch" in url:
            import urllib.parse
            return f"https://www.facebook.com/plugins/video.php?href={urllib.parse.quote(url)}&show_text=false"
        if "instagram.com" in url:
            return f"{url.split('?')[0].rstrip('/')}/embed"
        return url

    @property
    def whatsapp_message(self):
        return f"Hello! I'm interested in ordering *{self.name}* priced at {self.formatted_price}. Is it available?"


class AdminUser(UserMixin, db.Model):
    __tablename__ = "admin_users"
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active     = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))


class Inquiry(db.Model):
    __tablename__ = "inquiries"
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(120), nullable=False)
    phone      = db.Column(db.String(30), default="")
    subject    = db.Column(db.String(200), default="General Inquiry")
    message    = db.Column(db.Text, nullable=False)
    is_read    = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Testimonial(db.Model):
    __tablename__ = "testimonials"
    id            = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    location      = db.Column(db.String(120), default="Ilorin, Kwara State")
    message       = db.Column(db.Text, nullable=False)
    rating        = db.Column(db.Integer, default=5)
    is_approved   = db.Column(db.Boolean, default=False)
    created_at    = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))