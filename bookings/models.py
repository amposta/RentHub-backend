from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from marketplace.models import RentalItem
from decimal import Decimal

User = get_user_model()


class Booking(models.Model):
    """Rental booking/reservation"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_as_renter')
    item = models.ForeignKey(RentalItem, on_delete=models.CASCADE, related_name='bookings')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_as_owner')
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    special_requests = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['renter', 'status']),
            models.Index(fields=['owner', 'status']),
        ]
    
    def __str__(self):
        return f"Booking {self.id} - {self.item.title}"
    
    def get_duration_days(self):
        """Calculate number of rental days"""
        return (self.end_date - self.start_date).days + 1
    
    def save(self, *args, **kwargs):
        # Auto-populate owner from item
        if not self.owner_id:
            self.owner = self.item.owner
        
        # Calculate total price if not set
        if not self.total_price:
            days = self.get_duration_days()
            self.total_price = Decimal(days) * self.item.price_per_day
        
        super().save(*args, **kwargs)


class Payment(models.Model):
    """Payment tracking for bookings"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    stripe_charge_id = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    failed_reason = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment for Booking {self.booking.id}"
