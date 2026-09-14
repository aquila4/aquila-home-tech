"""
app/blueprints/admin/routes.py
Single image per product. Cloudinary for storage.
"""
from slugify import slugify
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.blueprints.admin import admin_bp
from app.models import AdminUser, Product, Category, Inquiry, Testimonial
from app.forms import LoginForm, ProductForm, CategoryForm, TestimonialForm
from app.utils import save_product_image, delete_product_image


# ── Auth ──────────────────────────────────────────────────────────────────────
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(request.args.get("next") or url_for("admin.dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("admin.login"))


# ── Dashboard ─────────────────────────────────────────────────────────────────
@admin_bp.route("/")
@login_required
def dashboard():
    stats = {
        "total_products":        Product.query.count(),
        "active_products":       Product.query.filter_by(is_active=True).count(),
        "featured_products":     Product.query.filter_by(featured=True).count(),
        "total_categories":      Category.query.count(),
        "total_inquiries":       Inquiry.query.count(),
        "unread_inquiries":      Inquiry.query.filter_by(is_read=False).count(),
        "total_testimonials":    Testimonial.query.count(),
        "approved_testimonials": Testimonial.query.filter_by(is_approved=True).count(),
    }
    recent_products  = Product.query.order_by(Product.created_at.desc()).limit(5).all()
    recent_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).limit(5).all()
    return render_template(
        "dashboard.html",
        stats=stats,
        recent_products=recent_products,
        recent_inquiries=recent_inquiries,
    )


# ── Products ──────────────────────────────────────────────────────────────────
@admin_bp.route("/products")
@login_required
def products():
    page     = request.args.get("page", 1, type=int)
    products = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template("products_list.html", products=products)


@admin_bp.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():
    form = ProductForm()
    form.category_id.choices = [
        (c.id, c.name) for c in Category.query.order_by(Category.name).all()
    ]

    if form.validate_on_submit():
        # Generate unique slug
        slug = slugify(form.name.data)
        base_slug, i = slug, 1
        while Product.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{i}"
            i += 1

        # Upload image to Cloudinary
        image_url = "default_product.jpg"
        uploaded_file = request.files.get("image")
        if uploaded_file and uploaded_file.filename:
            image_url = save_product_image(uploaded_file)

        product = Product(
            name           = form.name.data,
            slug           = slug,
            category_id    = form.category_id.data,
            description    = form.description.data or "",
            specifications = form.specifications.data or "",
            price          = form.price.data,
            old_price      = form.old_price.data,
            stock_quantity = form.stock_quantity.data,
            featured       = form.featured.data,
            is_active      = form.is_active.data,
            image          = image_url,
        )
        db.session.add(product)
        db.session.commit()
        flash(f"✅ Product '{product.name}' added successfully!", "success")
        return redirect(url_for("admin.products"))

    return render_template("product_form.html", form=form, action="Add")


@admin_bp.route("/products/<int:pid>/edit", methods=["GET", "POST"])
@login_required
def edit_product(pid: int):
    product = Product.query.get_or_404(pid)
    form    = ProductForm(obj=product)
    form.category_id.choices = [
        (c.id, c.name) for c in Category.query.order_by(Category.name).all()
    ]

    if form.validate_on_submit():
        product.name           = form.name.data
        product.category_id    = form.category_id.data
        product.description    = form.description.data or ""
        product.specifications = form.specifications.data or ""
        product.price          = form.price.data
        product.old_price      = form.old_price.data
        product.stock_quantity = form.stock_quantity.data
        product.featured       = form.featured.data
        product.is_active      = form.is_active.data

        # Only replace image if a new one is uploaded
        uploaded_file = request.files.get("image")
        if uploaded_file and uploaded_file.filename:
            # Delete old image from Cloudinary
            delete_product_image(product.image)
            # Upload new image to Cloudinary
            new_url       = save_product_image(uploaded_file)
            product.image = new_url

        db.session.commit()
        flash(f"✅ Product '{product.name}' updated successfully!", "success")
        return redirect(url_for("admin.products"))

    return render_template(
        "product_form.html",
        form=form,
        product=product,
        action="Edit"
    )


@admin_bp.route("/products/<int:pid>/delete", methods=["POST"])
@login_required
def delete_product(pid: int):
    product = Product.query.get_or_404(pid)
    delete_product_image(product.image)
    db.session.delete(product)
    db.session.commit()
    flash(f"Product '{product.name}' deleted.", "warning")
    return redirect(url_for("admin.products"))


@admin_bp.route("/products/<int:pid>/toggle-featured", methods=["POST"])
@login_required
def toggle_featured(pid: int):
    product          = Product.query.get_or_404(pid)
    product.featured = not product.featured
    db.session.commit()
    status = "featured" if product.featured else "unfeatured"
    flash(f"'{product.name}' is now {status}.", "info")
    return redirect(url_for("admin.products"))


# ── Categories ────────────────────────────────────────────────────────────────
@admin_bp.route("/categories")
@login_required
def categories():
    cats = Category.query.order_by(Category.name).all()
    return render_template("categories.html", categories=cats)


@admin_bp.route("/categories/add", methods=["GET", "POST"])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        slug = slugify(form.name.data)
        if Category.query.filter_by(slug=slug).first():
            flash("A category with that name already exists.", "danger")
        else:
            cat = Category(
                name        = form.name.data,
                slug        = slug,
                icon        = form.icon.data or "🛒",
                description = form.description.data or "",
            )
            db.session.add(cat)
            db.session.commit()
            flash(f"Category '{cat.name}' added!", "success")
            return redirect(url_for("admin.categories"))
    return render_template("category_form.html", form=form, action="Add")


@admin_bp.route("/categories/<int:cid>/edit", methods=["GET", "POST"])
@login_required
def edit_category(cid: int):
    cat  = Category.query.get_or_404(cid)
    form = CategoryForm(obj=cat)
    if form.validate_on_submit():
        cat.name        = form.name.data
        cat.slug        = slugify(form.name.data)
        cat.icon        = form.icon.data or "🛒"
        cat.description = form.description.data or ""
        db.session.commit()
        flash(f"Category '{cat.name}' updated!", "success")
        return redirect(url_for("admin.categories"))
    return render_template("category_form.html", form=form, cat=cat, action="Edit")


@admin_bp.route("/categories/<int:cid>/delete", methods=["POST"])
@login_required
def delete_category(cid: int):
    cat = Category.query.get_or_404(cid)
    if cat.product_count > 0:
        flash("Cannot delete a category that has products.", "danger")
    else:
        db.session.delete(cat)
        db.session.commit()
        flash(f"Category '{cat.name}' deleted.", "warning")
    return redirect(url_for("admin.categories"))


# ── Inquiries ─────────────────────────────────────────────────────────────────
@admin_bp.route("/inquiries")
@login_required
def inquiries():
    page      = request.args.get("page", 1, type=int)
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template("inquiries.html", inquiries=inquiries)


@admin_bp.route("/inquiries/<int:iid>")
@login_required
def inquiry_detail(iid: int):
    inquiry         = Inquiry.query.get_or_404(iid)
    inquiry.is_read = True
    db.session.commit()
    return render_template("inquiry_detail.html", inquiry=inquiry)


@admin_bp.route("/inquiries/<int:iid>/delete", methods=["POST"])
@login_required
def delete_inquiry(iid: int):
    inquiry = Inquiry.query.get_or_404(iid)
    db.session.delete(inquiry)
    db.session.commit()
    flash("Inquiry deleted.", "warning")
    return redirect(url_for("admin.inquiries"))


# ── Testimonials ──────────────────────────────────────────────────────────────
@admin_bp.route("/testimonials")
@login_required
def testimonials():
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template("testimonials.html", testimonials=testimonials)


@admin_bp.route("/testimonials/add", methods=["GET", "POST"])
@login_required
def add_testimonial():
    form = TestimonialForm()
    if form.validate_on_submit():
        t = Testimonial(
            customer_name = form.customer_name.data,
            location      = form.location.data or "Ilorin, Kwara State",
            message       = form.message.data,
            rating        = form.rating.data,
            is_approved   = form.is_approved.data,
        )
        db.session.add(t)
        db.session.commit()
        flash("Testimonial added!", "success")
        return redirect(url_for("admin.testimonials"))
    return render_template("testimonial_form.html", form=form, action="Add")


@admin_bp.route("/testimonials/<int:tid>/edit", methods=["GET", "POST"])
@login_required
def edit_testimonial(tid: int):
    t    = Testimonial.query.get_or_404(tid)
    form = TestimonialForm(obj=t)
    if form.validate_on_submit():
        t.customer_name = form.customer_name.data
        t.location      = form.location.data or "Ilorin, Kwara State"
        t.message       = form.message.data
        t.rating        = form.rating.data
        t.is_approved   = form.is_approved.data
        db.session.commit()
        flash("Testimonial updated!", "success")
        return redirect(url_for("admin.testimonials"))
    return render_template("testimonial_form.html", form=form, t=t, action="Edit")


@admin_bp.route("/testimonials/<int:tid>/delete", methods=["POST"])
@login_required
def delete_testimonial(tid: int):
    t = Testimonial.query.get_or_404(tid)
    db.session.delete(t)
    db.session.commit()
    flash("Testimonial deleted.", "warning")
    return redirect(url_for("admin.testimonials"))


@admin_bp.route("/testimonials/<int:tid>/toggle", methods=["POST"])
@login_required
def toggle_testimonial(tid: int):
    t             = Testimonial.query.get_or_404(tid)
    t.is_approved = not t.is_approved
    db.session.commit()
    status = "approved" if t.is_approved else "hidden"
    flash(f"Testimonial by {t.customer_name} is now {status}.", "info")
    return redirect(url_for("admin.testimonials"))