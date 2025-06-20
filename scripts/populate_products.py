#!/usr/bin/env python3
"""
Script to populate the database with sample products for the AEVI skincare store
"""

from app import create_app, db
from app.models import Product


def populate_products():
    """Add sample products to the database"""
    app = create_app()
    with app.app_context():
        sample_products = [
            Product(
                name="Nourishing Face Oil",
                price=39.99,
                category="Serums & Oils",
                description="A deeply nourishing facial oil infused with Nordic botanicals. Rich in antioxidants and essential fatty acids to restore skin's natural radiance.",
                short_description="Deeply nourishing facial oil with Nordic botanicals",
                image_main="/static/images/AEVI/Cards/Card1_2.png",
                image_hover="/static/images/AEVI/Cards/Card1_2.png",
                is_bestseller=True,
                is_new=False,
                rating=4.8,
                review_count=127,
                in_stock=True,
                ingredients="Jojoba Oil, Rosehip Seed Oil, Sea Buckthorn Oil, Vitamin E, Cloudberry Extract",
                how_to_use="Apply 2-3 drops to clean face morning and evening. Gently massage until absorbed.",
                benefits="Deeply hydrates, reduces fine lines, improves skin texture and radiance",
                size_options="15ml, 30ml",
                tags="anti-aging, hydrating, natural, organic"
            ),
            Product(
                name="Gentle Cleansing Foam",
                price=24.99,
                category="Cleansers & Masks",
                description="A gentle, pH-balanced cleansing foam that removes impurities while maintaining skin's natural moisture barrier.",
                short_description="Gentle pH-balanced cleansing foam",
                image_main="/static/images/AEVI/Cards/Card1_2.png",
                image_hover="/static/images/AEVI/Cards/Card1_2.png",
                is_bestseller=True,
                is_new=False,
                rating=4.6,
                review_count=89,
                in_stock=True,
                ingredients="Coconut-derived cleansers, Aloe Vera, Chamomile Extract, Glycerin",
                how_to_use="Apply to damp skin, massage gently, rinse with lukewarm water.",
                benefits="Cleanses without stripping, soothes sensitive skin, maintains pH balance",
                size_options="150ml, 300ml",
                tags="gentle, sensitive-skin, daily-use"
            ),
            Product(
                name="Brightening Vitamin C Serum",
                price=44.99,
                category="Serums & Oils",
                description="Powerful vitamin C serum with stabilized L-ascorbic acid to brighten skin and protect against environmental damage.",
                short_description="Brightening vitamin C serum with antioxidants",
                image_main="/static/images/AEVI/Cards/Card1_2.png",
                image_hover="/static/images/AEVI/Cards/Card1_2.png",
                is_bestseller=False,
                is_new=True,
                rating=4.7,
                review_count=56,
                in_stock=True,
                ingredients="15% L-Ascorbic Acid, Vitamin E, Ferulic Acid, Hyaluronic Acid",
                how_to_use="Apply 2-3 drops to clean skin in the morning. Follow with sunscreen.",
                benefits="Brightens complexion, reduces dark spots, provides antioxidant protection",
                size_options="30ml",
                tags="brightening, vitamin-c, antioxidant, morning-routine"
            ),
            Product(
                name="Hydrating Night Mask",
                price=32.99,
                category="Cleansers & Masks",
                description="An overnight hydrating mask that works while you sleep to restore and rejuvenate your skin.",
                short_description="Overnight hydrating mask for skin restoration",
                image_main="/static/images/AEVI/Cards/Card1_2.png",
                image_hover="/static/images/AEVI/Cards/Card1_2.png",
                is_bestseller=False,
                is_new=True,
                rating=4.5,
                review_count=34,
                in_stock=True,
                ingredients="Hyaluronic Acid, Peptides, Nordic Berry Extracts, Ceramides",
                how_to_use="Apply generously to clean skin before bed. Leave on overnight, rinse in morning.",
                benefits="Intense hydration, skin repair, improves elasticity and firmness",
                size_options="50ml",
                tags="hydrating, night-care, anti-aging, peptides"
            ),
            Product(
                name="Repair Balm",
                price=28.99,
                category="Balms",
                description="Multi-purpose repair balm for dry, damaged, or irritated skin. Perfect for lips, cuticles, and dry patches.",
                short_description="Multi-purpose repair balm for dry skin",
                image_main="/static/images/AEVI/Cards/Card1_2.png",
                image_hover="/static/images/AEVI/Cards/Card1_2.png",
                is_bestseller=True,
                is_new=False,
                rating=4.9,
                review_count=203,
                in_stock=True,
                ingredients="Shea Butter, Beeswax, Calendula Extract, Chamomile Oil",
                how_to_use="Apply to dry or irritated areas as needed. Safe for lips and sensitive areas.",
                benefits="Soothes irritation, repairs damaged skin, long-lasting moisture",
                size_options="15g, 30g",
                tags="healing, multi-purpose, sensitive-skin, natural"
            ),
            Product(
                name="Exfoliating Treatment",
                price=36.99,
                category="Treatments",
                description="Gentle yet effective exfoliating treatment with natural fruit acids to reveal smoother, brighter skin.",
                short_description="Gentle exfoliating treatment with fruit acids",
                image_main="/static/images/AEVI/Cards/Card1_2.png",
                image_hover="/static/images/AEVI/Cards/Card1_2.png",
                is_bestseller=False,
                is_new=False,
                rating=4.4,
                review_count=67,
                in_stock=True,
                ingredients="Lactic Acid, Glycolic Acid, Papaya Extract, Aloe Vera",
                how_to_use="Use 2-3 times per week on clean skin. Apply thin layer, leave for 5-10 minutes, rinse off.",
                benefits="Removes dead skin cells, improves texture, promotes cell renewal",
                size_options="75ml",
                tags="exfoliating, brightening, weekly-treatment, aha"
            ),
            Product(
                name="Body Moisturizer Nordic",
                price=22.99,
                category="Body",
                description="Rich, fast-absorbing body moisturizer infused with Nordic botanicals to nourish and protect your skin.",
                short_description="Rich body moisturizer with Nordic botanicals",
                image_main="/static/images/AEVI/Cards/Card1_2.png",
                image_hover="/static/images/AEVI/Cards/Card1_2.png",
                is_bestseller=False,
                is_new=False,
                rating=4.3,
                review_count=45,
                in_stock=True,
                ingredients="Nordic Sea Buckthorn, Birch Extract, Shea Butter, Coconut Oil",
                how_to_use="Apply to clean, dry skin daily. Massage until fully absorbed.",
                benefits="Long-lasting hydration, improves skin elasticity, non-greasy formula",
                size_options="200ml, 400ml",
                tags="body-care, hydrating, fast-absorbing, daily-use"
            ),
            Product(
                name="Eye Cream Renewal",
                price=48.99,
                category="Treatments",
                description="Intensive eye cream targeting fine lines, dark circles, and puffiness with peptides and caffeine.",
                short_description="Intensive eye cream for fine lines and dark circles",
                image_main="/static/images/AEVI/Cards/Card1_2.png",
                image_hover="/static/images/AEVI/Cards/Card1_2.png",
                is_bestseller=True,
                is_new=False,
                rating=4.6,
                review_count=112,
                in_stock=True,
                ingredients="Peptides, Caffeine, Hyaluronic Acid, Retinol Alternative, Vitamin K",
                how_to_use="Gently pat around eye area morning and evening using ring finger.",
                benefits="Reduces fine lines, diminishes dark circles, firms eye area",
                size_options="15ml",
                tags="eye-care, anti-aging, peptides, dark-circles"
            ),
            Product(
                name="Purifying Clay Mask",
                price=29.99,
                category="Cleansers & Masks",
                description="Deep-cleansing clay mask with Nordic white clay to purify pores and balance oily skin.",
                short_description="Deep-cleansing clay mask with Nordic white clay",
                image_main="/static/images/AEVI/Cards/Card1_2.png",
                image_hover="/static/images/AEVI/Cards/Card1_2.png",
                is_bestseller=False,
                is_new=True,
                rating=4.2,
                review_count=23,
                in_stock=True,
                ingredients="Nordic White Clay, Tea Tree Oil, Salicylic Acid, Chamomile",
                how_to_use="Apply to clean skin 1-2 times per week. Leave for 10-15 minutes, rinse with warm water.",
                benefits="Purifies pores, controls oil, reduces breakouts, balances skin",
                size_options="75ml",
                tags="purifying, oily-skin, acne-prone, weekly-treatment"
            ),
            Product(
                name="Lip Balm Set Nordic",
                price=18.99,
                category="Balms",
                description="Set of three nourishing lip balms with natural Nordic ingredients. Available in Original, Berry, and Mint.",
                short_description="Set of three nourishing lip balms",
                image_main="/static/images/AEVI/Cards/Card1_2.png",
                image_hover="/static/images/AEVI/Cards/Card1_2.png",
                is_bestseller=False,
                is_new=False,
                rating=4.7,
                review_count=78,
                in_stock=True,
                ingredients="Beeswax, Coconut Oil, Shea Butter, Nordic Berry Extracts, Vitamin E",
                how_to_use="Apply to lips as needed throughout the day.",
                benefits="Long-lasting moisture, prevents chapping, natural ingredients",
                size_options="3 x 4.5g",
                tags="lip-care, natural, set, gift-ready"
            ),
            Product(
                name="Toning Mist",
                price=26.99,
                category="Treatments",
                description="Refreshing toning mist with Nordic spring water and botanical extracts to balance and hydrate skin.",
                short_description="Refreshing toning mist with Nordic botanicals",
                image_main="/static/images/AEVI/Cards/Card1_2.png",
                image_hover="/static/images/AEVI/Cards/Card1_2.png",
                is_bestseller=False,
                is_new=True,
                rating=4.1,
                review_count=19,
                in_stock=True,
                ingredients="Nordic Spring Water, Rose Water, Witch Hazel, Hyaluronic Acid",
                how_to_use="Spray on clean face or over makeup throughout the day.",
                benefits="Balances pH, provides instant hydration, sets makeup",
                size_options="100ml, 200ml",
                tags="toning, hydrating, makeup-setting, refreshing"
            ),
            Product(
                name="Hand Cream Nordic Herbs",
                price=16.99,
                category="Body",
                description="Intensive hand cream with Nordic herbs and oils to protect and nourish hardworking hands.",
                short_description="Intensive hand cream with Nordic herbs",
                image_main="/static/images/AEVI/Cards/Card1_2.png",
                image_hover="/static/images/AEVI/Cards/Card1_2.png",
                is_bestseller=False,
                is_new=False,
                rating=4.5,
                review_count=61,
                in_stock=True,
                ingredients="Nordic Herbs Blend, Lanolin, Glycerin, Allantoin",
                how_to_use="Apply to hands as needed, especially after washing.",
                benefits="Intensive moisture, protects against dryness, non-greasy",
                size_options="50ml, 100ml",
                tags="hand-care, intensive, herbs, daily-use"
            )
        ]

        # Add products to session
        for product in sample_products:
            # Check if product already exists (by name)
            existing = Product.query.filter_by(name=product.name).first()
            if not existing:
                db.session.add(product)
                print(f"Added product: {product.name}")
            else:
                print(f"Product already exists: {product.name}")

        # Commit changes
        try:
            db.session.commit()
            print(f"\n✅ Successfully populated database with {len(sample_products)} products!")
            print("Products added:")
            for product in sample_products:
                print(f"  - {product.name} (${product.price})")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Error populating database: {e}")


if __name__ == "__main__":
    populate_products()