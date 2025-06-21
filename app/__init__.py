from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS

from config import Config

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.signin'


def create_app():
    app = Flask(__name__)

    # Load all config from config.py
    app.config.from_object(Config)

    print("Loaded DB URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # Initialize Flask extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    CORS(app)

    # Register routes
    from app.routes import (
        static_routes, product_routes, cart_routes,
         auth_routes, form_routes, user_routes
    )
    app.register_blueprint(static_routes.bp)
    app.register_blueprint(product_routes.bp)
    app.register_blueprint(cart_routes.bp)
    # app.register_blueprint(wishlist_routes.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(form_routes.bp)
    app.register_blueprint(user_routes.bp)

    # Custom Jinja helpers
    from app.utils.helpers import generate_stars
    app.jinja_env.globals.update(generate_stars=generate_stars)

    return app
