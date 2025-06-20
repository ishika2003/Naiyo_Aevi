from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.signin'


def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///aevi.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    CORS(app)

    # Register blueprints
    from app.routes import static_routes, product_routes, cart_routes, wishlist_routes, auth_routes, form_routes, \
        user_routes
    app.register_blueprint(static_routes.bp)
    app.register_blueprint(product_routes.bp)
    app.register_blueprint(cart_routes.bp)
    app.register_blueprint(wishlist_routes.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(form_routes.bp)
    app.register_blueprint(user_routes.bp)

    # Register custom Jinja filters
    from app.utils.helpers import generate_stars
    app.jinja_env.globals.update(generate_stars=generate_stars)

    return app