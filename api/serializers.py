from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import VerificationRequest
from bookings.models import Booking
from marketplace.models import Category, RentalItem

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon']


class SimpleUserSerializer(serializers.ModelSerializer):
    can_rent = serializers.ReadOnlyField()
    can_list_items = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'avatar',
            'is_verified',
            'is_identity_verified',
            'is_payout_connected',
            'can_rent',
            'can_list_items',
        ]


class RentalItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    owner = SimpleUserSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = RentalItem
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'price_per_day',
            'security_deposit',
            'dynamic_attributes',
            'location',
            'city',
            'state',
            'condition',
            'is_available',
            'average_rating',
            'total_bookings',
            'created_at',
            'updated_at',
            'category',
            'owner',
            'main_image',
            'images',
        ]

    def get_images(self, obj):
        return [image.url for image in obj.get_images() if image]

    def get_main_image(self, obj):
        image = obj.get_main_image()
        return image.url if image else None


class AdminUserSerializer(serializers.ModelSerializer):
    can_rent = serializers.ReadOnlyField()
    can_list_items = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'is_verified',
            'is_identity_verified',
            'is_payout_connected',
            'stripe_account_id',
            'can_rent',
            'can_list_items',
            'is_staff',
            'is_superuser',
            'date_joined',
        ]


class AdminVerificationRequestSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    reviewed_by = SimpleUserSerializer(read_only=True)

    class Meta:
        model = VerificationRequest
        fields = [
            'id',
            'user',
            'status',
            'document',
            'submitted_at',
            'reviewed_at',
            'reviewed_by',
            'admin_notes',
        ]


class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'display_order', 'is_active', 'created_at']
        read_only_fields = ['created_at']


class AdminRentalItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    owner = SimpleUserSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = RentalItem
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'price_per_day',
            'security_deposit',
            'dynamic_attributes',
            'location',
            'city',
            'state',
            'condition',
            'is_available',
            'average_rating',
            'total_bookings',
            'created_at',
            'updated_at',
            'category',
            'owner',
            'main_image',
            'images',
        ]
        read_only_fields = ['slug', 'average_rating', 'total_bookings', 'created_at', 'updated_at', 'category', 'owner']

    def get_images(self, obj):
        return [image.url for image in obj.get_images() if image]

    def get_main_image(self, obj):
        image = obj.get_main_image()
        return image.url if image else None


class AdminBookingSerializer(serializers.ModelSerializer):
    renter = SimpleUserSerializer(read_only=True)
    owner = SimpleUserSerializer(read_only=True)
    item = AdminRentalItemSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'renter',
            'owner',
            'item',
            'start_date',
            'end_date',
            'total_price',
            'status',
            'created_at',
            'updated_at',
            'confirmed_at',
            'completed_at',
            'special_requests',
        ]
        read_only_fields = ['created_at', 'updated_at', 'confirmed_at', 'completed_at', 'renter', 'owner', 'item', 'total_price']
