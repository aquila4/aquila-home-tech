"""
app/models.py – SQLAlchemy ORM models.

Models:
  Category   – product categories
  Product    – the store catalogue
  AdminUser  – back-office user (Flask-Login)
  Inquiry    – contact-form submissions
  Testimonial – customer reviews
"""
from datetime import datetime, timezone
from slugify import slugify
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


# ─────────────────────────────────────────────────────────────────────────────
# Category
# ─────────────────────────────────────────────────────────────────────────────
class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(120), nullable=False, unique=True, index=True)
    icon = db.Column(db.String(10), default="🛒")          # emoji icon
    description = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # relationship
    products = db.relationship("Product", backref="category", lazy="dynamic")

    def __repr__(self):
        return f"<Category {self.name}>"

    @property
    def product_count(self):
        return self.products.count()


# ─────────────────────────────────────────────────────────────────────────────
# Product
# ─────────────────────────────────────────────────────────────────────────────
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), nullable=False, unique=True, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    description = db.Column(db.Text, default="")
    specifications = db.Column(db.Text, default="")   # stored as plain text / markdown
    price = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    old_price = db.Column(db.Numeric(12, 2), nullable=True)   # for discount display
    image = db.Column(db.String(300), default="default_product.jpg")
    stock_quantity = db.Column(db.Integer, default=0)
    featured = db.Column(db.Boolean, default=False, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Product {self.name}>"

    # ── Helpers ──────────────────────────────────────────────────────────────
    def generate_slug(self):
        self.slug = slugify(self.name)

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
    def whatsapp_message(self):
        return (
            f"Hello! I'm interested in ordering *{self.name}* "
            f"priced at {self.formatted_price}. "
            f"Is it available? Please let me know."
        )


# ─────────────────────────────────────────────────────────────────────────────
# AdminUser
# ─────────────────────────────────────────────────────────────────────────────
class AdminUser(UserMixin, db.Model):
    __tablename__ = "admin_users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<AdminUser {self.username}>"


@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))


# ─────────────────────────────────────────────────────────────────────────────
# Inquiry  (contact-form submissions)
# ─────────────────────────────────────────────────────────────────────────────
class Inquiry(db.Model):
    __tablename__ = "inquiries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), default="")
    subject = db.Column(db.String(200), default="General Inquiry")
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Inquiry from {self.name}>"


# ─────────────────────────────────────────────────────────────────────────────
# Testimonial
# ─────────────────────────────────────────────────────────────────────────────
class Testimonial(db.Model):
    __tablename__ = "testimonials"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), default="Ilorin, Kwara State")
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)     # 1–5 stars
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Testimonial by {self.customer_name}>"
