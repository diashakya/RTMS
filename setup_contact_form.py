#!/usr/bin/env python3
"""
Setup script for Contact form functionality
"""
import os
import sys
import subprocess

def setup_contact_form():
    """Set up the contact form functionality"""
    print("🔧 Setting Up Contact Form Functionality")
    print("=" * 45)
    
    # Change to the Django project directory
    project_dir = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu"
    os.chdir(project_dir)
    
    try:
        # 1. Create migrations
        print("1️⃣ Creating database migrations...")
        result = subprocess.run([sys.executable, 'manage.py', 'makemigrations'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migrations created successfully")
            print(result.stdout)
        else:
            print("❌ Error creating migrations:")
            print(result.stderr)
            return False
        
        # 2. Apply migrations
        print("\n2️⃣ Applying database migrations...")
        result = subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migrations applied successfully")
        else:
            print("❌ Error applying migrations:")
            print(result.stderr)
            return False
        
        print("\n🎉 Contact form setup completed successfully!")
        
        print("\n📋 What's now available:")
        print("✅ Contact form model (Contact)")
        print("✅ Contact form class (ContactForm)")
        print("✅ Functional contact view")
        print("✅ Admin interface for viewing messages")
        print("✅ Email notifications (optional)")
        print("✅ Form validation and error handling")
        
        print("\n🚀 Features:")
        print("- Users can submit feedback/inquiries")
        print("- Form validation for all fields")
        print("- Success/error messages")
        print("- Admin can view all messages")
        print("- Mark messages as read/unread")
        print("- Email notifications to admin")
        
        print("\n🧪 Test the contact form:")
        print("1. Start Django server: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000/contact/")
        print("3. Fill out and submit the form")
        print("4. Check admin: http://127.0.0.1:8000/admin/main/contact/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return False

def create_sample_contact_data():
    """Create some sample contact data for testing"""
    print("\n📝 Creating sample contact data...")
    
    try:
        # Setup Django environment
        sys.path.insert(0, r'c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')
        
        import django
        django.setup()
        
        from main.models import Contact
        
        # Create sample contacts
        sample_contacts = [
            {
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '+977-9860123456',
                'message': 'I love your restaurant! The food quality is excellent. Keep up the good work!'
            },
            {
                'name': 'Sarah Wilson',
                'email': 'sarah@example.com',
                'phone': '+977-9860654321',
                'message': 'Hi, I would like to inquire about catering services for a party of 50 people.'
            },
            {
                'name': 'Mike Johnson',
                'email': 'mike@example.com',
                'phone': '+977-9860789012',
                'message': 'The delivery was a bit late yesterday, but the food was still hot and delicious!'
            }
        ]
        
        created_count = 0
        for contact_data in sample_contacts:
            contact, created = Contact.objects.get_or_create(
                email=contact_data['email'],
                defaults=contact_data
            )
            if created:
                created_count += 1
                print(f"✅ Created contact from {contact.name}")
        
        print(f"📊 Created {created_count} sample contact messages")
        print("You can view them in the admin panel!")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")

if __name__ == "__main__":
    print("🚀 CONTACT FORM SETUP")
    print("=" * 30)
    
    if setup_contact_form():
        create_sample_contact_data()
        print("\n🎉 Setup completed successfully!")
        print("Your contact form is now fully functional!")
    else:
        print("\n❌ Setup failed. Please check the errors above.")