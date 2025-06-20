def generate_stars(rating):
    """Generate star rating display"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    stars = '★' * full_stars
    if half_star:
        stars += '☆'

    return stars