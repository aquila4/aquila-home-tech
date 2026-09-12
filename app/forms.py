"""
app/forms.py - WTForms form definitions.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, DecimalField, IntegerField,
    BooleanField, SelectField, PasswordField, EmailField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 80)])
    password = PasswordField("Password", validators=[DataRequired()])


class ProductForm(FlaskForm):
    name           = StringField("Product Name", validators=[DataRequired(), Length(2, 200)])
    category_id    = SelectField("Category", coerce=int, validators=[DataRequired()])
    description    = TextAreaField("Description", validators=[Optional()])
    specifications = TextAreaField("Specifications", validators=[Optional()])
    price          = DecimalField("Price (₦)", validators=[DataRequired(), NumberRange(min=0)])
    old_price      = DecimalField("Old Price (₦)", validators=[Optional(), NumberRange(min=0)])
    stock_quantity = IntegerField("Stock Quantity", validators=[DataRequired(), NumberRange(min=0)], default=0)
    featured       = BooleanField("Featured Product")
    is_active      = BooleanField("Active (visible in store)", default=True)
    video_url      = StringField("Video URL", validators=[Optional(), Length(max=500)])
    image          = FileField(
        "Product Image",
        validators=[
            Optional(),
            FileAllowed(["jpg", "jpeg", "png", "gif", "webp"], "Images only!"),
        ],
    )


class CategoryForm(FlaskForm):
    name        = StringField("Category Name", validators=[DataRequired(), Length(2, 100)])
    icon        = StringField("Icon (emoji)", validators=[Optional(), Length(max=10)])
    description = TextAreaField("Description", validators=[Optional()])


class ContactForm(FlaskForm):
    name    = StringField("Full Name", validators=[DataRequired(), Length(2, 120)])
    email   = EmailField("Email Address", validators=[DataRequired(), Email()])
    phone   = StringField("Phone Number", validators=[Optional(), Length(max=30)])
    subject = StringField("Subject", validators=[Optional(), Length(max=200)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(10, 2000)])


class TestimonialForm(FlaskForm):
    customer_name = StringField("Customer Name", validators=[DataRequired(), Length(2, 120)])
    location      = StringField("Location", validators=[Optional(), Length(max=120)])
    message       = TextAreaField("Testimonial", validators=[DataRequired(), Length(10, 1000)])
    rating        = SelectField(
        "Rating",
        choices=[(1,"1 ★"),(2,"2 ★★"),(3,"3 ★★★"),(4,"4 ★★★★"),(5,"5 ★★★★★")],
        coerce=int, default=5,
    )
    is_approved = BooleanField("Approved (visible on site)")


class SearchForm(FlaskForm):
    class Meta:
        csrf = False
    q        = StringField("Search", validators=[Optional()])
    category = StringField("Category", validators=[Optional()])