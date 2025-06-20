from flask import Blueprint, jsonify, request, redirect, url_for, flash
from app import db, mail
from app.models import Lead, Newsletter, User
from flask_mail import Message

bp = Blueprint('forms', __name__)


@bp.route('/submit-contact', methods=['POST'])
def submit_contact():
    """Handle contact form submission"""
    if request.is_json:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        phone = data.get('phone', '')
        subject = data.get('subject', '')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        phone = request.form.get('phone', '')
        subject = request.form.get('subject', '')

    lead = Lead(
        name=name,
        email=email,
        message=message,
        phone=phone,
        subject=subject
    )

    db.session.add(lead)
    db.session.commit()

    try:
        msg = Message(
            subject=f'New Contact Form Submission: {subject}',
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body=f'''
            New contact form submission:

            Name: {name}
            Email: {email}
            Phone: {phone}
            Subject: {subject}

            Message:
            {message}
            '''
        )
        mail.send(msg)
    except Exception as e:
        app.logger.error(f'Failed to send email: {e}')

    if request.is_json:
        return jsonify({'success': True, 'message': 'Thank you for your message!'})
    else:
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('static.thank_you'))


@bp.route('/subscribe-newsletter', methods=['POST'])
def subscribe_newsletter():
    """Handle newsletter subscription"""
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
    else:
        email = request.form.get('email')

    if not email:
        if request.is_json:
            return jsonify({'error': 'Email is required'}), 400
        else:
            flash('Email is required', 'error')
            return redirect(url_for('static.home'))

    existing = Newsletter.query.filter_by(email=email).first()
    if existing:
        if request.is_json:
            return jsonify({'message': 'Already subscribed!'})
        else:
            flash('You are already subscribed to our newsletter!', 'info')
            return redirect(url_for('static.home'))

    newsletter = Newsletter(email=email)
    db.session.add(newsletter)

    user = User.query.filter_by(email=email).first()
    if user:
        user.is_subscribed = True

    db.session.commit()

    try:
        msg = Message(
            subject='Welcome to AEVI Newsletter!',
            sender=app.config['MAIL_USERNAME'],
            recipients=[email],
            body='''
            Welcome to AEVI!

            Thank you for subscribing to our newsletter. 
            You'll receive exclusive updates about our Nordic skincare products.

            Enjoy 10% off your first order!

            Best regards,
            The AEVI Team
            '''
        )
        mail.send(msg)
    except Exception as e:
        app.logger.error(f'Failed to send welcome email: {e}')

    if request.is_json:
        return jsonify({'success': True, 'message': 'Successfully subscribed!'})
    else:
        flash('Successfully subscribed to our newsletter!', 'success')
        return redirect(url_for('static.home'))


@bp.route('/newsletter/unsubscribe', methods=['POST'])
def unsubscribe_newsletter():
    """Unsubscribe from newsletter"""
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    newsletter = Newsletter.query.filter_by(email=email).first()
    if newsletter:
        newsletter.is_active = False
        db.session.commit()

    user = User.query.filter_by(email=email).first()
    if user:
        user.is_subscribed = False
        db.session.commit()

    return jsonify({'success': True, 'message': 'Successfully unsubscribed from newsletter'})