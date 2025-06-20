from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

bp = Blueprint('auth', __name__)


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    subscribe_newsletter = BooleanField('Subscribe to Newsletter')


@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    """User sign in"""
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if request.is_json:
                return jsonify({'success': True, 'user': user.to_dict()})
            else:
                flash('Successfully signed in!', 'success')
                return redirect(url_for('static.home'))
        else:
            if request.is_json:
                return jsonify({'error': 'Invalid credentials'}), 401
            else:
                flash('Invalid email or password', 'error')
                return render_template('signin.html')

    return render_template('signin.html')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """User sign up"""
    form = SignupForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            subscribe_newsletter = form.subscribe_newsletter.data

            if User.query.filter_by(email=email).first():
                if request.is_json:
                    return jsonify({'error': 'Email already exists'}), 400
                flash('Email already registered', 'error')
                return render_template('signup.html', form=form)

            user = User(
                email=email,
                password_hash=generate_password_hash(password),
                first_name=first_name,
                last_name=last_name,
                is_subscribed=subscribe_newsletter
            )

            db.session.add(user)
            db.session.commit()

            login_user(user)

            if request.is_json:
                return jsonify({'success': True, 'user': user.to_dict()})
            flash('Account created successfully!', 'success')
            return redirect(url_for('static.home'))

        if request.is_json:
            return jsonify({'error': 'Invalid form data', 'errors': form.errors}), 400
        return render_template('signup.html', form=form)

    return render_template('signup.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('static.home'))


@bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html', user=current_user)