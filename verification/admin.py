from django.contrib import admin
from .models import TrustBadge


@admin.register(TrustBadge)
class TrustBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge_type', 'earned_at')
    list_filter = ('badge_type', 'earned_at')
    search_fields = ('user__email',)
    readonly_fields = ('earned_at',)
