"""
Setup script for FitBuddy
Helps with initial configuration and dependency installation
"""

import os
import sys
import subprocess


def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"Error: Python 3.8+ required. Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_dependencies():
    """Install required dependencies"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False


def setup_env_file():
    """Set up .env file from template"""
    print("\nSetting up environment variables...")
    
    if os.path.exists(".env"):
        print("✓ .env file already exists")
        overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != 'y':
            return True
    
    if not os.path.exists(".env.example"):
        print("✗ .env.example not found")
        return False
    
    # Copy template
    with open(".env.example", 'r') as f:
        content = f.read()
    
    with open(".env", 'w') as f:
        f.write(content)
    
    print("✓ Created .env file from template")
    print("\nIMPORTANT: Please edit .env file and add your OPENAI_API_KEY")
    print("You can get an API key from: https://platform.openai.com/api-keys")
    
    return True


def verify_setup():
    """Verify that setup is complete"""
    print("\nVerifying setup...")
    
    checks = []
    
    # Check .env file
    if os.path.exists(".env"):
        checks.append(("✓ .env file exists", True))
    else:
        checks.append(("✗ .env file missing", False))
    
    # Check for API key
    has_api_key = False
    if os.path.exists(".env"):
        with open(".env", 'r') as f:
            content = f.read()
            if "OPENAI_API_KEY=" in content and "your_openai_api_key_here" not in content:
                has_api_key = True
    
    if has_api_key:
        checks.append(("✓ OPENAI_API_KEY configured", True))
    else:
        checks.append(("✗ OPENAI_API_KEY not configured", False))
    
    # Check knowledge base
    if os.path.exists("knowledge_base"):
        checks.append(("✓ knowledge_base directory exists", True))
    else:
        checks.append(("✗ knowledge_base directory missing", False))
    
    # Print results
    for check, passed in checks:
        print(check)
    
    all_passed = all(passed for _, passed in checks)
    
    if all_passed:
        print("\n✓ Setup complete! You can now run: python main.py")
    else:
        print("\n✗ Setup incomplete. Please address the issues above.")
    
    return all_passed


def main():
    """Main setup function"""
    print("="*60)
    print("FitBuddy Setup")
    print("="*60 + "\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment file
    if not setup_env_file():
        sys.exit(1)
    
    # Verify setup
    verify_setup()
    
    print("\n" + "="*60)
    print("Setup complete!")
    print("="*60)


if __name__ == "__main__":
    main()
