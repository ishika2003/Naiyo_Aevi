#!/usr/bin/env python3
"""
Reset database script - Drops all tables and recreates them with new schema
"""

import os
from app import create_app, db


def reset_database():
    """Drop all tables and recreate with new schema"""
    app = create_app()
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()

        print("Creating new tables...")
        db.create_all()

        print("Database reset complete!")


if __name__ == '__main__':
    # Remove the database file if it exists
    db_file = 'aevi.db'
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed {db_file}")

    reset_database()