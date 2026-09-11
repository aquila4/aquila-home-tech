"""
app/blueprints/main/routes.py – Home, About, Contact routes.
"""
from flask import render_template, request, flash, redirect, url_for, current_app

from app import db
from app.blueprints.main import main_bp
from app.models import Product, Category, Testimonial, Inquiry
from app.forms import ContactForm


# ─────────────────────────────────────────────────────────────────────────────
# Home
# ─────────────────────────────────────────────────────────────────────────────
@main_bp.route("/")
def index():
    featured_products = (
        Product.query.filter_by(featured=True, is_active=True)
        .order_by(Product.created_at.desc())
        .limit(8)
        .all()
    )
    latest_products = (
        Product.query.filter_by(is_active=True)
        .order_by(Product.created_at.desc())
        .limit(8)
        .all()
    )
    categories = Category.query.all()
    testimonials = (
        Testimonial.query.filter_by(is_approved=True)
        .order_by(Testimonial.created_at.desc())
        .limit(6)
        .all()
    )
    return render_template(
        "index.html",
        featured_products=featured_products,
        latest_products=latest_products,
        categories=categories,
        testimonials=testimonials,
    )


# ─────────────────────────────────────────────────────────────────────────────
# About
# ─────────────────────────────────────────────────────────────────────────────
@main_bp.route("/about")
def about():
    return render_template("about.html")


# ─────────────────────────────────────────────────────────────────────────────
# Contact
# ─────────────────────────────────────────────────────────────────────────────
@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        inquiry = Inquiry(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data or "",
            subject=form.subject.data or "General Inquiry",
            message=form.message.data,
        )
        db.session.add(inquiry)
        db.session.commit()
        flash("Thank you! Your message has been sent. We'll reply soon.", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html", form=form)
