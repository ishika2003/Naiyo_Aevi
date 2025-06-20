
# 🌿 AEVI – Nordic Skincare Platform

A Flask-based e-commerce site inspired by [liveaevi.com](https://liveaevi.com), with a complete backend and frontend integration.

## ✨ Features

### Frontend

* Multi-page: Home, Shop, About, Contact, Blog
* Responsive & SEO-friendly
* Dynamic product loading via Flask APIs
* Newsletter popup with 10% discount
* Real-time search & product filtering

### Backend (Flask + PostgreSQL)

* Clean routing & session management
* User auth (sign up/login)
* Admin dashboard for user/product management
* Contact form & newsletter (Flask-Mail)
* RESTful API integration

### E-commerce

* Product catalog with categories, badges
* Bestsellers, new items, star ratings
* Newsletter system + contact leads

### Security

* Password hashing (Werkzeug)
* CSRF protection, input validation
* Protected user routes

## 🚀 Quick Start

```bash
git clone https://github.com/ishika2003/Naiyo_Aevi.git
cd AEVI-main
pip install -r requirements.txt
cp .env.example .env  # update values
python init_db.py
python app.py
```

Access:

* Home: `http://localhost:5000`
* Shop: `/shop`, Contact: `/contact`, Dashboard: `/dashboard`

## 📁 Structure

```
AEVI-main/
├── app.py
├── templates/       # Jinja2 HTML templates
├── static/          # CSS, JS, images
├── init_db.py
├── requirements.txt
└── .env.example
```

## 🛠️ Deployment (Heroku)

```bash
echo "web: gunicorn app:app" > Procfile
git push heroku main
```

