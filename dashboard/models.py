from django.db import models
from django.contrib.auth import get_user_model
from bookings.models import Booking
from datetime import date

User = get_user_model()


class Earning(models.Model):
    """Track earnings for item owners"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earnings')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='earning')
    
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    paid_out = models.BooleanField(default=False)
    paid_out_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Earning {self.id} - ${self.net_amount}"
    
    def save(self, *args, **kwargs):
        # Calculate platform fee (10% by default)
        if not self.platform_fee:
            self.platform_fee = self.gross_amount * 0.10
            self.net_amount = self.gross_amount - self.platform_fee
        super().save(*args, **kwargs)


class Insight(models.Model):
    """Daily insights for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insights')
    date = models.DateField(default=date.today)
    
    views_count = models.IntegerField(default=0)
    inquiries_count = models.IntegerField(default=0)
    bookings_count = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'date')
    
    def __str__(self):
        return f"Insight for {self.user.email} - {self.date}"
