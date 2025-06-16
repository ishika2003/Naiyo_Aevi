#!/usr/bin/env python3
"""
Setup script for AEVI Flask application
Handles installation, database setup, and initial configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("="*60)
    print("🌿 AEVI Flask Application Setup")
    print("   Pure Nordic Skincare Platform")
    print("="*60)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def setup_environment():
    """Setup environment variables"""
    print("\n🔧 Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            # Copy example file
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your configuration:")
            print("   - Set your SECRET_KEY")
            print("   - Configure DATABASE_URL")
            print("   - Add email configuration for notifications")
        else:
            print("❌ .env.example file not found")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def setup_database():
    """Initialize database"""
    print("\n🗄️  Setting up database...")
    
    try:
        # Import and run database initialization
        from init_db import main as init_db
        init_db()
        print("✅ Database setup completed")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        print("💡 Make sure your database is running and credentials are correct")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "static/images/uploads",
        "logs",
        "backups"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")

def run_tests():
    """Run basic tests to verify setup"""
    print("\n🧪 Running basic tests...")
    
    try:
        # Test Flask app import
        from app import app
        
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page loads correctly")
            
            # Test API endpoint
            response = client.get('/api/products')
            if response.status_code == 200:
                print("✅ Products API works correctly")
        
        print("✅ All tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Tests failed: {e}")
        return False

def print_next_steps():
    """Print next steps for user"""
    print("\n" + "="*60)
    print("🎉 Setup completed successfully!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Edit .env file with your configuration")
    print("2. Start the development server:")
    print("   python app.py")
    print("\n🌐 Default URLs:")
    print("   Homepage: http://localhost:5000")
    print("   Shop: http://localhost:5000/shop")
    print("   About: http://localhost:5000/about")
    print("   Contact: http://localhost:5000/contact")
    print("\n🔐 Test user credentials:")
    print("   Email: admin@aevi.com")
    print("   Password: admin123")
    print("\n📚 For more information, check the README.md file")
    print("="*60)

def main():
    """Main setup function"""
    print_banner()
    
    # Check requirements
    check_python_version()
    
    # Setup steps
    install_dependencies()
    
    if not setup_environment():
        print("❌ Environment setup failed")
        sys.exit(1)
    
    create_directories()
    
    # Database setup (optional - user can skip if not ready)
    db_response = input("\n🗄️  Setup database now? (y/n): ").lower().strip()
    if db_response in ['y', 'yes']:
        if not setup_database():
            print("⚠️  Database setup failed, but you can run init_db.py later")
    else:
        print("⏭️  Skipping database setup. Run 'python init_db.py' when ready.")
    
    # Run tests (optional)
    test_response = input("\n🧪 Run tests? (y/n): ").lower().strip()
    if test_response in ['y', 'yes']:
        if not run_tests():
            print("⚠️  Some tests failed, but setup is complete")
    
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)