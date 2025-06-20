from app import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    image_main = db.Column(db.String(500), nullable=True)
    image_hover = db.Column(db.String(500), nullable=True)
    is_bestseller = db.Column(db.Boolean, default=False)
    is_new = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    in_stock = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    short_description = db.Column(db.String(500), nullable=True)
    ingredients = db.Column(db.Text, nullable=True)
    how_to_use = db.Column(db.Text, nullable=True)
    benefits = db.Column(db.Text, nullable=True)
    size_options = db.Column(db.Text, nullable=True)
    tags = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'short_description': self.short_description,
            'price': self.price,
            'category': self.category,
            'image_main': self.image_main,
            'image_hover': self.image_hover,
            'is_bestseller': self.is_bestseller,
            'is_new': self.is_new,
            'rating': self.rating,
            'review_count': self.review_count,
            'in_stock': self.in_stock,
            'ingredients': self.ingredients,
            'how_to_use': self.how_to_use,
            'benefits': self.benefits,
            'size_options': self.size_options,
            'tags': self.tags,
            'created_at': self.created_at.isoformat()
        }