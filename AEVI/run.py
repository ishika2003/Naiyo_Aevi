from app import create_app, db
from app.models import Product
from datetime import datetime


def init_db():
    """Initialize database with tables and sample data"""
    db.create_all()

    if Product.query.count() == 0:
        sample_products = [
            Product(
                name='NOURISHING FACE OIL',
                description='A luxurious face oil that deeply nourishes and restores radiance to tired, dull skin. Formulated with potent Nordic super berries rich in antioxidants and vitamins.',
                short_description='Radiance Enhancing Nordic Super Berries',
                price=98.00,
                category='serums-oils',
                image_main='static/images/nourishing-face-oil.jpg',
                image_hover='static/images/nourishing-face-oil.jpg',
                is_bestseller=True,
                rating=4.9,
                review_count=20,
                ingredients='Sea Buckthorn Oil, Cloudberry Seed Oil, Lingonberry Extract, Rosehip Oil, Vitamin E',
                how_to_use='Apply 2-3 drops to clean skin morning and evening. Gently massage until absorbed.',
                benefits='Brightens skin, reduces fine lines, improves elasticity, provides deep hydration',
                size_options='30ml',
                tags='bestseller,face oil,anti-aging,radiance,nordic berries'
            ),
            Product(
                name='HYALURONIC ACID FACE SERUM',
                description='An intensely hydrating serum that plumps and smooths skin with multiple molecular weights of hyaluronic acid, enhanced with Nordic seaweed extracts.',
                short_description='Super Hydrating Seaweed + Tremella',
                price=94.00,
                category='serums-oils',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                is_bestseller=True,
                rating=4.8,
                review_count=15,
                ingredients='Hyaluronic Acid (3 molecular weights), Tremella Mushroom Extract, Nordic Seaweed, Aloe Vera',
                how_to_use='Apply to clean skin before moisturizer, morning and evening.',
                benefits='Intense hydration, plumps fine lines, improves skin texture, long-lasting moisture',
                size_options='30ml',
                tags='bestseller,hyaluronic acid,hydration,serum,plumping'
            ),
            Product(
                name='ALL-OVER BALM',
                description='A multi-purpose healing balm that soothes, protects, and nourishes skin anywhere you need it. Perfect for dry patches, cuticles, and sensitive areas.',
                short_description='Everywhere Essential',
                price=24.00,
                category='balms',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                is_bestseller=True,
                rating=4.7,
                review_count=10,
                ingredients='Shea Butter, Coconut Oil, Beeswax, Calendula Extract, Chamomile Oil',
                how_to_use='Apply to dry or irritated skin as needed. Safe for face and body.',
                benefits='Soothes irritation, protects skin barrier, deeply moisturizes, versatile use',
                size_options='15ml',
                tags='bestseller,balm,healing,multi-purpose,sensitive skin'
            ),
            Product(
                name='CLARIFYING CLAY MASK',
                description='A powerful detoxifying mask formulated with natural Nordic blue clays that draw out impurities while gently exfoliating for clearer, smoother skin.',
                short_description='Detoxifying Natural Blue Clays',
                price=38.00,
                category='cleansers-masks',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                is_new=True,
                rating=4.6,
                review_count=8,
                ingredients='Nordic Blue Clay, Kaolin Clay, Charcoal Powder, Tea Tree Oil, Witch Hazel',
                how_to_use='Apply even layer to clean skin, avoid eye area. Leave for 10-15 minutes, rinse with warm water.',
                benefits='Deep cleanses pores, removes impurities, controls oil, improves skin texture',
                size_options='75ml',
                tags='new,clay mask,detox,pore care,deep cleanse'
            ),
            Product(
                name='EYE ELIXIR',
                description='A gentle yet effective eye treatment that brightens dark circles and reduces puffiness with awakening tea extracts and Nordic berries.',
                short_description='Awakening Tea Extracts + Brightening Berries',
                price=62.00,
                category='treatments',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                rating=4.5,
                review_count=12,
                ingredients='Green Tea Extract, Caffeine, Cloudberry Extract, Peptides, Niacinamide',
                how_to_use='Gently pat around eye area morning and evening using ring finger.',
                benefits='Reduces dark circles, minimizes puffiness, firms delicate skin, brightens eye area',
                size_options='15ml',
                tags='eye care,dark circles,puffiness,brightening,tea extracts'
            ),
            Product(
                name='LUMI BALM',
                description='A natural dewy highlighter that gives skin a subtle, healthy glow. Perfect for creating that effortless Nordic radiance.',
                short_description='Dewy Highlighter',
                price=28.00,
                category='balms',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                rating=4.4,
                review_count=6,
                ingredients='Coconut Oil, Mica, Jojoba Oil, Vitamin E, Natural Fragrance',
                how_to_use='Apply to high points of face: cheekbones, nose bridge, cupids bow.',
                benefits='Natural glow, buildable coverage, nourishing formula, long-lasting',
                size_options='8ml',
                tags='highlighter,glow,natural,radiance,makeup'
            ),
            Product(
                name='AWAKENING HAND & BODY WASH',
                description='An energizing cleansing gel infused with Nordic pine, eucalyptus, and frankincense to awaken your senses while gently cleansing.',
                short_description='Nordic Pine, Eucalyptus + Frankincense',
                price=15.00,
                category='body',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                rating=4.3,
                review_count=18,
                ingredients='Nordic Pine Extract, Eucalyptus Oil, Frankincense, Coconut-derived Cleansers',
                how_to_use='Apply to wet skin, lather, and rinse thoroughly. Use daily.',
                benefits='Gentle cleansing, energizing scent, natural ingredients, suitable for sensitive skin',
                size_options='50ml,250ml',
                tags='body wash,energizing,pine,eucalyptus,natural'
            ),
            Product(
                name='HYDRATING HAND & BODY LOTION',
                description='A deeply moisturizing lotion that absorbs quickly while providing long-lasting hydration with the same signature Nordic scent blend.',
                short_description='Nordic Pine, Eucalyptus + Frankincense',
                price=15.00,
                category='body',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                rating=4.2,
                review_count=14,
                ingredients='Shea Butter, Coconut Oil, Nordic Pine Extract, Eucalyptus Oil, Frankincense',
                how_to_use='Apply to clean skin, massage until absorbed. Use daily or as needed.',
                benefits='Deep hydration, fast absorption, long-lasting moisture, signature scent',
                size_options='50ml,250ml',
                tags='body lotion,hydrating,fast absorbing,signature scent'
            )
        ]

        for product in sample_products:
            db.session.add(product)

        db.session.commit()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        init_db()
    app.run(debug=True)