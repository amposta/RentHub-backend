from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TrustBadge(models.Model):
    """Trust badges earned by users"""
    BADGE_CHOICES = [
        ('email_verified', 'Email Verified'),
        ('phone_verified', 'Phone Verified'),
        ('id_verified', 'ID Verified'),
        ('super_renter', 'Super Renter'),
        ('super_host', 'Super Host'),
        ('trusted_seller', 'Trusted Seller'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trust_badges')
    badge_type = models.CharField(max_length=50, choices=BADGE_CHOICES)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'badge_type')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.get_badge_type_display()}"
