#!/usr/bin/env python3
"""
Database initialization script for AEVI Flask application
Creates tables and populates with sample data based on the live website
"""

from app import app, db, User, Product, Newsletter, Lead
from werkzeug.security import generate_password_hash
import sys

def create_tables():
    """Create all database tables"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")

def populate_sample_data():
    """Populate database with sample data matching the live website"""
    with app.app_context():
        # Clear existing data
        db.session.query(Product).delete()
        db.session.query(User).delete()
        db.session.query(Newsletter).delete()
        db.session.query(Lead).delete()
        
        # Create sample users
        users = [
            User(
                email='admin@aevi.com',
                password_hash=generate_password_hash('admin123'),
                first_name='Admin',
                last_name='User',
                is_subscribed=True
            ),
            User(
                email='user@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='John',
                last_name='Doe',
                is_subscribed=True
            ),
            User(
                email='jane@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Jane',
                last_name='Smith',
                is_subscribed=False
            )
        ]
        
        for user in users:
            db.session.add(user)
        
        # Create sample products based on the live website
        products = [
            # Bestsellers
            Product(
                name='Nourishing Face Oil',
                description='Radiance Enhancing Nordic Super Berries',
                price=98.00,
                category='serums-oils',
                image_main='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-NourishingFaceOil-09.png?v=1743785875&width=500',
                image_hover='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-NourishingFaceOil-Awards_2b0bd624-a72a-44c6-b5ae-fc903dd73fa6.jpg?v=1736768182&width=500',
                is_bestseller=True,
                is_new=False,
                rating=4.8,
                review_count=20,
                in_stock=True
            ),
            Product(
                name='Hyaluronic Acid Face Serum',
                description='Super Hydrating Seaweed + Tremella',
                price=94.00,
                category='serums-oils',
                image_main='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-HyaluronicFaceSerum-02.jpg?v=1736768094&width=500',
                image_hover='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-HyaluronicFaceSerum-Awards_cb45a317-9f90-48e3-a9da-3010e4384c87.jpg?v=1736768094&width=500',
                is_bestseller=True,
                is_new=False,
                rating=4.9,
                review_count=10,
                in_stock=True
            ),
            Product(
                name='All-Over Balm',
                description='Everywhere Essential',
                price=24.00,
                category='balms',
                image_main='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-AllOverBalm-02.jpg?v=1736855490&width=500',
                image_hover='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-AllOverBalm-01-New.jpg?v=1736773328&width=500',
                is_bestseller=True,
                is_new=False,
                rating=4.7,
                review_count=10,
                in_stock=True
            ),
            Product(
                name='Eye Elixir',
                description='Awakening Tea Extracts + Brightening Berries',
                price=62.00,
                category='treatments',
                image_main='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-EyeElixir-02_8a439651-f69e-465d-8d16-034aba3531ca.jpg?v=1736768123&width=500',
                image_hover='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-EyeElixir-01_810f343f-8250-46b2-a2d2-0e1bef6bca8b.jpg?v=1736768123&width=500',
                is_bestseller=True,
                is_new=False,
                rating=4.6,
                review_count=2,
                in_stock=True
            ),
            
            # New Products
            Product(
                name='Clarifying Clay Mask',
                description='Detoxifying Natural Blue Clays',
                price=38.00,
                category='cleansers-masks',
                image_main='https://liveaevi.com/cdn/shop/files/Aevi-Social-Bean-FaceMask-01.jpg?v=1743785498&width=500',
                image_hover='https://liveaevi.com/cdn/shop/files/Aevi-Web-Products-ClarifyingClayMask-01-New_9de21f89-723d-4e1f-bcfb-647a947afe0d.jpg?v=1736785406&width=500',
                is_bestseller=False,
                is_new=True,
                rating=4.5,
                review_count=1,
                in_stock=True
            ),
            Product(
                name='Cloud Bag',
                description='Stylish and functional beauty bag',
                price=22.00,
                category='merch',
                image_main='https://liveaevi.com/cdn/shop/files/Aevi-Web-CloudBag-Small-04.png?v=1746376088&width=500',
                image_hover='https://liveaevi.com/cdn/shop/files/Aevi-Web-CloudBag-Large-01.png?v=1746372270&width=500',
                is_bestseller=False,
                is_new=True,
                rating=0.0,
                review_count=0,
                in_stock=True
            ),
            
            # Body Care
            Product(
                name='Awakening Hand & Body Wash',
                description='Nordic Pine, Eucalyptus + Frankincense',
                price=15.00,
                category='body',
                image_main='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-HandandBodyWash-03.jpg?v=1736790918&width=500',
                image_hover='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-AwakeningHandandBodyWash-01_d7156a23-8989-4c33-b569-d09b5177590b.jpg?v=1736785296&width=500',
                is_bestseller=False,
                is_new=False,
                rating=4.2,
                review_count=5,
                in_stock=True
            ),
            Product(
                name='Hydrating Hand & Body Lotion',
                description='Deeply moisturizing Nordic formula',
                price=28.00,
                category='body',
                image_main='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-HandandBodyLotion-02.jpg?v=1741103175&width=500',
                image_hover='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-HandandBodyLotion-04.jpg?v=1741103274&width=500',
                is_bestseller=False,
                is_new=False,
                rating=4.3,
                review_count=7,
                in_stock=True
            ),
            
            # Treatments
            Product(
                name='Blemish Treatment',
                description='Fast Acting Spot Treatment',
                price=28.00,
                category='treatments',
                image_main='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-BlemishTreatment-02.jpg?v=1736768030&width=500',
                image_hover='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-BlemishTreatment-01.jpg?v=1736768030&width=500',
                is_bestseller=False,
                is_new=False,
                rating=4.4,
                review_count=3,
                in_stock=True
            ),
            
            # Bundles/Sets
            Product(
                name='The Hydrate + Nourish Duo',
                description='Ultimate Skin Nourishment',
                price=172.00,
                category='gifts-sets',
                image_main='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-NourishingFaceOil-07.png?v=1743785875&width=500',
                image_hover='https://liveaevi.com/cdn/shop/files/Aevi-Web-Products-HydrateandNourishDuo-Awards.jpg?v=1734623399&width=500',
                is_bestseller=True,
                is_new=False,
                rating=4.9,
                review_count=33,
                in_stock=True
            ),
            Product(
                name='The Body Travel Essentials',
                description='Nordic Pine, Eucalyptus + Frankincense',
                price=25.00,
                category='gifts-sets',
                image_main='https://liveaevi.com/cdn/shop/files/Aevi-Web-TraveWash-01.png?v=1741103274&width=500',
                image_hover='https://liveaevi.com/cdn/shop/files/Aevi-Website-New-Products-WashLotionTravelDuo-01-New.jpg?v=1736785129&width=500',
                is_bestseller=False,
                is_new=False,
                rating=4.1,
                review_count=9,
                in_stock=True
            ),
            Product(
                name='The Radiance + Repair Balm Kit',
                description='Essentials On The Go',
                price=47.00,
                category='gifts-sets',
                image_main='https://liveaevi.com/cdn/shop/files/Aevi-Website-Products-AllOverBalm-03.jpg?v=1736855490&width=500',
                image_hover='https://liveaevi.com/cdn/shop/files/Aevi-Website-New-Products-BalmDuo-01-New.jpg?v=1736773291&width=500',
                is_bestseller=False,
                is_new=False,
                rating=4.3,
                review_count=14,
                in_stock=True
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        # Add sample newsletter subscribers
        newsletter_subscribers = [
            Newsletter(email='admin@aevi.com'),
            Newsletter(email='user@example.com'),
            Newsletter(email='newsletter@example.com'),
            Newsletter(email='skincare@example.com')
        ]
        
        for subscriber in newsletter_subscribers:
            db.session.add(subscriber)
        
        # Add sample leads/contacts
        sample_leads = [
            Lead(
                name='Sarah Johnson',
                email='sarah@example.com',
                subject='Product Inquiry',
                message='I have sensitive skin and would like to know which products would work best for me.',
                phone='+1234567890'
            ),
            Lead(
                name='Michael Brown',
                email='michael@example.com',
                subject='Partnership',
                message='I am interested in becoming a retailer for AEVI products.',
                phone='+1234567891'
            )
        ]
        
        for lead in sample_leads:
            db.session.add(lead)
        
        # Commit all changes
        db.session.commit()
        print("✅ Sample data populated successfully!")
        
        # Print summary
        print(f"\n📊 Database Summary:")
        print(f"   Users: {User.query.count()}")
        print(f"   Products: {Product.query.count()}")
        print(f"   Newsletter Subscribers: {Newsletter.query.count()}")
        print(f"   Leads: {Lead.query.count()}")
        print(f"\n🔐 Test User Credentials:")
        print(f"   Admin: admin@aevi.com / admin123")
        print(f"   User: user@example.com / password123")
        print(f"   User: jane@example.com / password123")

def main():
    """Main function to initialize database"""
    print("🚀 Initializing AEVI Database...")
    
    try:
        create_tables()
        populate_sample_data()
        print("\n✅ Database initialization completed successfully!")
        print("\n🌐 You can now run the Flask app with: python app.py")
        print("🔗 Visit: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()