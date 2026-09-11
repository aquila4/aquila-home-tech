# 🦅 Aquila Home Tech

**Quality Electronics & Home Appliances You Can Trust**

A production-ready Flask web application for Aquila Home Tech — an electronics and home
appliances store based in Ilorin, Kwara State, Nigeria.

---

## 📋 Table of Contents

1. [Requirements](#requirements)
2. [Quick Start (Local)](#quick-start-local)
3. [Project Structure](#project-structure)
4. [Admin Dashboard](#admin-dashboard)
5. [Environment Variables](#environment-variables)
6. [Deployment](#deployment)

---

## ✅ Requirements

| Tool | Minimum Version |
|------|----------------|
| Python | 3.10+ |
| pip | 22+ |

> **No database server needed for local development** — SQLite is used by default.

---

## 🚀 Quick Start (Local)

Follow these steps exactly, in order.

### Step 1 – Download & unzip

Unzip the downloaded file, then open a terminal inside the project folder:

```bash
cd aquila_home_tech
```

### Step 2 – Create a virtual environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

You should see `(venv)` at the start of your terminal prompt.

### Step 3 – Install dependencies

```bash
pip install -r requirements.txt
```

This installs Flask, SQLAlchemy, Flask-Login, Pillow, and all other packages.

### Step 4 – Create your environment file

```bash
# macOS / Linux
cp .env.example .env

# Windows
copy .env.example .env
```

The default `.env` works out of the box for local development. You can open it in any
text editor and change the `SECRET_KEY` if you like.

### Step 5 – Generate the default product image

```bash
python generate_placeholder.py
```

### Step 6 – Run the application

```bash
python run.py
```

You should see:

```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 7 – Open in your browser

| Page | URL |
|------|-----|
| Home | http://localhost:5000 |
| Products | http://localhost:5000/products |
| About | http://localhost:5000/about |
| Contact | http://localhost:5000/contact |
| **Admin** | **http://localhost:5000/admin** |

---

## 🔐 Admin Dashboard

Default login credentials (change these in `.env` before going live):

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `Admin@1234!` |

From the admin panel you can:
- Add, edit, delete products with image upload
- Manage categories
- View and reply to customer inquiries
- Manage and approve testimonials

---

## 📁 Project Structure

```
aquila_home_tech/
├── run.py                          # Entry point
├── config.py                       # Dev / Prod / Test configs
├── requirements.txt
├── .env.example                    # Copy to .env
├── generate_placeholder.py         # Run once to create default image
│
├── instance/
│   └── aquila.db                   # SQLite database (auto-created)
│
└── app/
    ├── __init__.py                 # App factory
    ├── models.py                   # DB models
    ├── forms.py                    # WTForms
    ├── utils.py                    # Image helpers
    │
    ├── blueprints/
    │   ├── main/routes.py          # Home, About, Contact
    │   ├── products/routes.py      # Catalogue, Detail
    │   └── admin/routes.py         # Full CRUD dashboard
    │
    ├── static/
    │   ├── css/main.css            # Public styles
    │   ├── css/admin.css           # Admin styles
    │   ├── js/main.js              # Public JS
    │   ├── js/admin.js             # Admin JS
    │   └── images/
    │       ├── default_product.jpg # Fallback image
    │       └── uploads/            # Uploaded product images
    │
    └── templates/
        ├── base.html
        ├── index.html
        ├── about.html
        ├── contact.html
        ├── partials/               # navbar, footer, product_card
        ├── products/               # catalogue, detail
        ├── errors/                 # 404, 500
        └── admin/                  # Full admin panel templates
```

---

## ⚙️ Environment Variables

Open `.env` to configure:

```env
FLASK_ENV=development          # development | production
SECRET_KEY=your-secret-here    # Change this in production!

# Database (SQLite default; swap for PostgreSQL in production)
DATABASE_URL=sqlite:///aquila.db
# DATABASE_URL=postgresql://user:password@localhost:5432/aquila_db

# Admin credentials (used only on first run)
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@aquilahometech.com
ADMIN_PASSWORD=Admin@1234!

# Business info (shown in templates)
WHATSAPP_NUMBER=2348012345678
BUSINESS_PHONE=+234 801 234 5678
BUSINESS_EMAIL=info@aquilahometech.com
BUSINESS_ADDRESS=12 Electronics Road, GRA, Ilorin, Kwara State, Nigeria
```

---

## 🌐 Deployment (Production)

### Option A – Render.com (free tier)

1. Push the project to a GitHub repository
2. Create a new **Web Service** on [render.com](https://render.com)
3. Set **Build Command:** `pip install -r requirements.txt`
4. Set **Start Command:** `gunicorn run:app`
5. Add all environment variables from `.env` in the Render dashboard
6. Change `DATABASE_URL` to a PostgreSQL connection string (Render provides free PostgreSQL)

### Option B – VPS / Ubuntu Server

```bash
# Install dependencies
sudo apt update && sudo apt install python3-pip python3-venv nginx -y

# Clone / upload your project to /var/www/aquila_home_tech

cd /var/www/aquila_home_tech
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit with production values

# Run with Gunicorn
gunicorn --workers 4 --bind 0.0.0.0:8000 run:app

# Set up Nginx as reverse proxy (see nginx docs)
```

### Switching to PostgreSQL

1. Install: `pip install psycopg2-binary`
2. Update `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/aquila_db
   ```
3. Run `flask db upgrade` (Flask-Migrate is already configured)

---

## 📞 Business Contact

- **WhatsApp:** +234 801 234 5678
- **Email:** info@aquilahometech.com
- **Location:** Ilorin, Kwara State, Nigeria

---

*Built with Flask · Bootstrap 5 · SQLite/PostgreSQL · Python 3*
