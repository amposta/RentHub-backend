from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from getpass import getpass

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser with email-based authentication'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address for the superuser',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the superuser',
        )
        parser.add_argument(
            '--first-name',
            type=str,
            default='Admin',
            help='First name for the superuser',
        )
        parser.add_argument(
            '--last-name',
            type=str,
            default='User',
            help='Last name for the superuser',
        )
    
    def handle(self, *args, **options):
        email = options.get('email')
        password = options.get('password')
        first_name = options.get('first_name')
        last_name = options.get('last_name')
        
        # Prompt for email if not provided
        if not email:
            email = input('Email: ').strip()
        
        # Validate email
        if not email or '@' not in email:
            raise CommandError('Invalid email address')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            raise CommandError(f'User with email {email} already exists')
        
        # Prompt for password if not provided
        if not password:
            password = getpass('Password: ')
            password_confirm = getpass('Password (confirm): ')
            
            if password != password_confirm:
                raise CommandError('Passwords do not match')
        
        # Validate password
        if len(password) < 8:
            raise CommandError('Password must be at least 8 characters long')
        
        # Create superuser
        try:
            user = User.objects.create_superuser(
                email=email,
                username=email.split('@')[0],  # Use email prefix as username
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Superuser created successfully!\n'
                    f'  Email: {user.email}\n'
                    f'  Username: {user.username}'
                )
            )
        except Exception as e:
            raise CommandError(f'Error creating superuser: {str(e)}')
