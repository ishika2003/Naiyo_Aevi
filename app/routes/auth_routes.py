from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from app.utils.helpers import send_email, generate_token, confirm_token
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__)

CONFIRM_SALT = 'email-confirmation-salt'
RESET_SALT = 'password-reset-salt'

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

            # Send confirmation email
            token = generate_token(user.email, CONFIRM_SALT)
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)
            html = f'<p>Click to confirm your email: <a href="{confirm_url}">{confirm_url}</a></p>'
            send_email('Confirm Your Email', [user.email], html)

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


@bp.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token, CONFIRM_SALT)
    if not email:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('auth.signin'))
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_confirmed:
        flash('Account already confirmed. Please login.', 'info')
    else:
        user.is_confirmed = True
        user.confirmed_on = datetime.utcnow()
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('auth.signin'))


@bp.route('/resend-confirmation')
def resend_confirmation():
    if not current_user.is_authenticated:
        flash('Please login first.', 'error')
        return redirect(url_for('auth.signin'))
    token = generate_token(current_user.email, CONFIRM_SALT)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = f'<p>Click to confirm your email: <a href="{confirm_url}">{confirm_url}</a></p>'
    send_email('Confirm Your Email', [current_user.email], html)
    flash('A new confirmation email has been sent.', 'info')
    return redirect(url_for('auth.dashboard'))


@bp.route('/request-reset', methods=['GET', 'POST'])
def request_reset():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_token(user.email, RESET_SALT)
            reset_url = url_for('auth.reset_with_token', token=token, _external=True)
            html = f'<p>Click to reset your password: <a href="{reset_url}">{reset_url}</a></p>'
            send_email('Password Reset Request', [user.email], html)
        flash('If your email is registered, you will receive a password reset link.', 'info')
        return redirect(url_for('auth.signin'))
    return render_template('request_reset.html')


@bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    email = confirm_token(token, RESET_SALT)
    if not email:
        flash('The reset link is invalid or has expired.', 'error')
        return redirect(url_for('auth.request_reset'))
    user = User.query.filter_by(email=email).first_or_404()
    if request.method == 'POST':
        password = request.form.get('password')
        user.password_hash = generate_password_hash(password)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.signin'))
    return render_template('reset_password.html', token=token)