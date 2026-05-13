from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from marketplace.models import Category, RentalItem
from decimal import Decimal
import random

User = get_user_model()

CATEGORIES = [
    {'name': 'Cars', 'icon': '🚗', 'display_order': 1},
    {'name': 'Cameras', 'icon': '📷', 'display_order': 2},
    {'name': 'Appliances', 'icon': '🏠', 'display_order': 3},
    {'name': 'Sports Gear', 'icon': '⚽', 'display_order': 4},
    {'name': 'Tools', 'icon': '🔧', 'display_order': 5},
    {'name': 'Fashion', 'icon': '👗', 'display_order': 6},
    {'name': 'Electronics', 'icon': '📱', 'display_order': 7},
]

ITEMS = [
    # Cars
    {'title': 'Toyota Fortuner 2022', 'category': 'Cars', 'price': Decimal('65'), 'location': 'San Francisco, CA', 'city': 'San Francisco', 'state': 'CA'},
    {'title': 'Honda Civic 2021', 'category': 'Cars', 'price': Decimal('55'), 'location': 'Los Angeles, CA', 'city': 'Los Angeles', 'state': 'CA'},
    {'title': 'BMW 3 Series 2021', 'category': 'Cars', 'price': Decimal('85'), 'location': 'San Francisco, CA', 'city': 'San Francisco', 'state': 'CA'},
    
    # Cameras
    {'title': 'Sony A7 IV Camera', 'category': 'Cameras', 'price': Decimal('45'), 'location': 'New York, NY', 'city': 'New York', 'state': 'NY'},
    {'title': 'Canon RF 50mm Lens', 'category': 'Cameras', 'price': Decimal('20'), 'location': 'San Francisco, CA', 'city': 'San Francisco', 'state': 'CA'},
    {'title': 'GoPro Hero 11', 'category': 'Cameras', 'price': Decimal('35'), 'location': 'Austin, TX', 'city': 'Austin', 'state': 'TX'},
    
    # Tools
    {'title': 'DeWalt Cordless Drill', 'category': 'Tools', 'price': Decimal('15'), 'location': 'Austin, TX', 'city': 'Austin', 'state': 'TX'},
    {'title': 'Makita Power Saw', 'category': 'Tools', 'price': Decimal('25'), 'location': 'Denver, CO', 'city': 'Denver', 'state': 'CO'},
    {'title': 'Bosch Rotary Hammer', 'category': 'Tools', 'price': Decimal('30'), 'location': 'Seattle, WA', 'city': 'Seattle', 'state': 'WA'},
    
    # Sports
    {'title': 'Paddle Board', 'category': 'Sports Gear', 'price': Decimal('18'), 'location': 'Bay Area, CA', 'city': 'Bay Area', 'state': 'CA'},
    {'title': 'Mountain Bike', 'category': 'Sports Gear', 'price': Decimal('16'), 'location': 'Colorado, CO', 'city': 'Colorado', 'state': 'CO'},
    {'title': 'Camping Tent 4-Person', 'category': 'Sports Gear', 'price': Decimal('12'), 'location': 'Denver, CO', 'city': 'Denver', 'state': 'CO'},
    
    # Electronics
    {'title': 'JBL Charge 5', 'category': 'Electronics', 'price': Decimal('8'), 'location': 'San Francisco, CA', 'city': 'San Francisco', 'state': 'CA'},
    {'title': 'Apple AirPods Pro', 'category': 'Electronics', 'price': Decimal('5'), 'location': 'New York, NY', 'city': 'New York', 'state': 'NY'},
    {'title': 'Sony WH-1000XM5 Headphones', 'category': 'Electronics', 'price': Decimal('12'), 'location': 'Austin, TX', 'city': 'Austin', 'state': 'TX'},
    
    # Appliances
    {'title': 'Dyson Vacuum Cleaner', 'category': 'Appliances', 'price': Decimal('20'), 'location': 'San Francisco, CA', 'city': 'San Francisco', 'state': 'CA'},
    {'title': 'Instant Pot', 'category': 'Appliances', 'price': Decimal('10'), 'location': 'Los Angeles, CA', 'city': 'Los Angeles', 'state': 'CA'},
    {'title': 'Air Fryer', 'category': 'Appliances', 'price': Decimal('12'), 'location': 'Seattle, WA', 'city': 'Seattle', 'state': 'WA'},
    
    # Fashion
    {'title': 'Designer Handbag', 'category': 'Fashion', 'price': Decimal('15'), 'location': 'New York, NY', 'city': 'New York', 'state': 'NY'},
    {'title': 'Formal Dress', 'category': 'Fashion', 'price': Decimal('25'), 'location': 'Los Angeles, CA', 'city': 'Los Angeles', 'state': 'CA'},
]


class Command(BaseCommand):
    help = 'Seed the database with initial categories and mock rental items'
    
    def handle(self, *args, **options):
        self.stdout.write('Starting to seed database...')
        
        # Create categories
        self.stdout.write('Creating categories...')
        for cat_data in CATEGORIES:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'display_order': cat_data['display_order'],
                }
            )
            if created:
                self.stdout.write(f"✓ Created category: {category.name}")
            else:
                self.stdout.write(f"• Category already exists: {category.name}")
        
        # Create a test user (owner)
        self.stdout.write('Creating test owner user...')
        owner, created = User.objects.get_or_create(
            email='owner@example.com',
            defaults={
                'username': 'owner_user',
                'first_name': 'Test',
                'last_name': 'Owner',
            }
        )
        if created:
            owner.set_password('password123')
            owner.save()
            self.stdout.write(f"✓ Created owner: {owner.email}")
        else:
            self.stdout.write(f"• Owner already exists: {owner.email}")
        
        # Create rental items
        self.stdout.write(f'Creating {len(ITEMS)} mock rental items...')
        for item_data in ITEMS:
            category = Category.objects.get(name=item_data['category'])
            
            item, created = RentalItem.objects.get_or_create(
                title=item_data['title'],
                owner=owner,
                defaults={
                    'category': category,
                    'description': f"High-quality {item_data['title']}. Perfect for your needs. Well-maintained and ready to use.",
                    'price_per_day': item_data['price'],
                    'location': item_data['location'],
                    'city': item_data['city'],
                    'state': item_data['state'],
                    'condition': random.choice(['like_new', 'excellent', 'good']),
                    'is_available': random.choice([True, True, True, False]),  # 75% available
                    'image1': 'placeholder.jpg',  # You'll need to add actual images
                }
            )
            
            if created:
                self.stdout.write(f"✓ Created item: {item.title}")
            else:
                self.stdout.write(f"• Item already exists: {item.title}")
        
        self.stdout.write(self.style.SUCCESS('✓ Database seeding completed successfully!'))
