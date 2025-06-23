from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from app import mail

def generate_stars(rating):
    """Generate star rating display"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    stars = '★' * full_stars
    if half_star:
        stars += '☆'

    return stars

def send_email(subject, recipients, html_body):
    msg = Message(subject, recipients=recipients, html=html_body)
    mail.send(msg)

def generate_token(email, salt):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=salt)

def confirm_token(token, salt, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=salt, max_age=expiration)
    except Exception:
        return False
    return email