from django.contrib import admin
from .models import Booking, Payment


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'renter', 'start_date', 'end_date', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at', 'start_date')
    search_fields = ('renter__email', 'owner__email', 'item__title')
    readonly_fields = ('total_price', 'created_at', 'updated_at', 'confirmed_at', 'completed_at')
    actions = ['confirm_booking', 'complete_booking', 'cancel_booking']
    
    def confirm_booking(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='confirmed', confirmed_at=timezone.now())
        self.message_user(request, "Booking confirmed!")
    
    def complete_booking(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, "Booking marked as completed!")
    
    def cancel_booking(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, "Booking cancelled!")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'status', 'created_at', 'paid_at')
    list_filter = ('status', 'created_at')
    search_fields = ('booking__id', 'stripe_charge_id')
    readonly_fields = ('created_at', 'stripe_payment_intent_id', 'stripe_charge_id')
