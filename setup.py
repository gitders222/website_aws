#!/usr/bin/env python3
"""
Setup script for Flask Portfolio
This script creates the necessary directory structure and placeholder files.
"""

import os
import shutil
import sys
from pathlib import Path

def create_directory_structure():
    """Create the necessary directory structure for the portfolio project."""
    print("Creating directory structure...")
    
    # Create main directories
    directories = [
        "data",
        "static/css",
        "static/js",
        "static/img",
        "static/img/projects",
        "templates",
        "templates/admin"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created {directory}/")
    
    print("Directory structure created successfully.")

def create_placeholder_images():
    """Create placeholder text files for images."""
    print("\nCreating placeholder files for images...")
    
    image_placeholders = [
        "static/img/profile.jpg",
        "static/img/hero-bg.jpg",
        "static/img/projects/ecommerce.jpg",
        "static/img/projects/taskmanager.jpg"
    ]
    
    for image in image_placeholders:
        with open(image + ".placeholder", "w") as f:
            f.write(f"# Placeholder for {image}\n")
            f.write("# Replace this with an actual image file.\n")
        print(f"✓ Created placeholder for {image}")
    
    print("Placeholder files created successfully.")
    print("\nNOTE: You need to replace these placeholder files with actual images.")

def check_files():
    """Check if the necessary application files exist."""
    print("\nChecking for application files...")
    
    required_files = [
        "app.py",
        "static/css/style.css",
        "static/js/script.js",
        "templates/base.html",
        "templates/index.html",
        "templates/about.html",
        "templates/projects.html",
        "templates/project_detail.html",
        "templates/blog.html",
        "templates/blog_post.html",
        "templates/contact.html",
        "templates/testimonials.html",
        "templates/admin/dashboard.html"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("The following required files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("\nPlease make sure to create these files before running the application.")
    else:
        print("All required application files are present.")

def main():
    """Main function to set up the project."""
    print("Flask Portfolio Setup\n")
    
    # Check if we're in the right directory
    if not Path("setup.py").is_file():
        print("Error: This script must be run from the project root directory.")
        sys.exit(1)
    
    create_directory_structure()
    create_placeholder_images()
    check_files()
    
    print("\nSetup completed!")
    print("\nNext steps:")
    print("1. Replace placeholder image files with actual images")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the application: python app.py")
    print("4. Access your portfolio at: http://127.0.0.1:5000/")

if __name__ == "__main__":
    main()