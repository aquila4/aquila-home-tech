"""
app/blueprints/products/routes.py – Product catalogue, detail, search.
"""
from urllib.parse import quote_plus
from flask import render_template, request, abort, current_app, url_for

from app.blueprints.products import products_bp
from app.models import Product, Category
from app.forms import SearchForm


# ─────────────────────────────────────────────────────────────────────────────
# Catalogue (with search + category filter + pagination)
# ─────────────────────────────────────────────────────────────────────────────
@products_bp.route("/")
def catalogue():
    form = SearchForm(request.args)
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("PRODUCTS_PER_PAGE", 12)

    query = Product.query.filter_by(is_active=True)

    # Category filter
    cat_slug = request.args.get("category", "").strip()
    active_category = None
    if cat_slug:
        active_category = Category.query.filter_by(slug=cat_slug).first()
        if active_category:
            query = query.filter_by(category_id=active_category.id)

    # Full-text search on name / description
    search_q = request.args.get("q", "").strip()
    if search_q:
        like = f"%{search_q}%"
        query = query.filter(
            (Product.name.ilike(like)) | (Product.description.ilike(like))
        )

    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    categories = Category.query.all()
    return render_template(
        "products/catalogue.html",
        products=products,
        categories=categories,
        active_category=active_category,
        search_q=search_q,
        form=form,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Product detail
# ─────────────────────────────────────────────────────────────────────────────
@products_bp.route("/<slug>")
def detail(slug: str):
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()

    # Related: same category, excluding current
    related = (
        Product.query.filter(
            Product.category_id == product.category_id,
            Product.id != product.id,
            Product.is_active == True,
        )
        .order_by(Product.created_at.desc())
        .limit(4)
        .all()
    )

    # Build WhatsApp link
    wa_msg = quote_plus(product.whatsapp_message)
    wa_link = f"https://wa.me/{current_app.config['WHATSAPP_NUMBER']}?text={wa_msg}"

    return render_template(
        "products/detail.html",
        product=product,
        related=related,
        wa_link=wa_link,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Category page (shortcut)
# ─────────────────────────────────────────────────────────────────────────────
@products_bp.route("/category/<slug>")
def by_category(slug: str):
    return catalogue()
