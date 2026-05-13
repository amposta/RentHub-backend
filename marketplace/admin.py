from django.contrib import admin
from .models import Category, RentalItem, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(RentalItem)
class RentalItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'price_per_day', 'is_available', 'total_bookings', 'created_at')
    list_filter = ('category', 'is_available', 'condition', 'created_at')
    search_fields = ('title', 'description', 'owner__email', 'city')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('total_bookings', 'total_revenue', 'average_rating', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'category', 'title', 'slug', 'description')
        }),
        ('Pricing & Availability', {
            'fields': ('price_per_day', 'is_available', 'condition')
        }),
        ('Images', {
            'fields': ('image1', 'image2', 'image3', 'image4', 'image5'),
            'classes': ('collapse',)
        }),
        ('Location', {
            'fields': ('location', 'city', 'state', 'latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('total_bookings', 'total_revenue', 'average_rating'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__email', 'item__title')
    readonly_fields = ('added_at',)
