from django.contrib import admin
from .models import Earning, Insight


@admin.register(Earning)
class EarningAdmin(admin.ModelAdmin):
    list_display = ('owner', 'gross_amount', 'platform_fee', 'net_amount', 'paid_out', 'created_at')
    list_filter = ('paid_out', 'created_at')
    search_fields = ('owner__email', 'booking__id')
    readonly_fields = ('platform_fee', 'net_amount', 'created_at')


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'views_count', 'bookings_count', 'revenue')
    list_filter = ('date',)
    search_fields = ('user__email',)
