from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, UserProfile, VerificationRequest


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_verified', 'overall_rating', 'date_joined')
    list_filter = ('is_verified', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone', 'avatar', 'is_verified', 'bio', 'location', 'overall_rating', 'total_reviews')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'id_verified', 'email_verified', 'phone_verified')
    list_filter = ('id_verified', 'email_verified', 'phone_verified', 'created_at')
    search_fields = ('user__email', 'city')
    readonly_fields = ('total_earnings', 'total_spent', 'created_at', 'updated_at')


@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'submitted_at', 'reviewed_at', 'reviewed_by')
    list_filter = ('status', 'submitted_at')
    search_fields = ('user__email',)
    readonly_fields = ('submitted_at',)
    actions = ['approve_verification', 'reject_verification']
    
    def approve_verification(self, request, queryset):
        for obj in queryset:
            obj.status = 'approved'
            obj.reviewed_by = request.user
            obj.reviewed_at = timezone.now()
            obj.save()
        self.message_user(request, "Verification approved!")
    approve_verification.short_description = "Approve selected verifications"
    
    def reject_verification(self, request, queryset):
        for obj in queryset:
            obj.status = 'rejected'
            obj.reviewed_by = request.user
            obj.reviewed_at = timezone.now()
            obj.save()
        self.message_user(request, "Verification rejected!")
    reject_verification.short_description = "Reject selected verifications"


from django.utils import timezone
