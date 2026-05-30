from django.urls import path
from .views import CategoryListAPIView, RentalItemDetailAPIView, RentalItemListAPIView
from .auth_views import SignupAPIView, LoginAPIView, LogoutAPIView, CurrentUserAPIView
from .admin_views import (
    AdminUserListAPIView,
    AdminVerificationRequestListAPIView,
    AdminVerificationRequestActionAPIView,
    AdminCategoryListCreateAPIView,
    AdminCategoryRetrieveUpdateDestroyAPIView,
    AdminRentalItemListAPIView,
    AdminRentalItemRetrieveUpdateAPIView,
    AdminBookingListAPIView,
    AdminBookingRetrieveUpdateAPIView,
)

urlpatterns = [
    # Auth endpoints
    path('auth/signup/', SignupAPIView.as_view(), name='api-signup'),
    path('auth/login/', LoginAPIView.as_view(), name='api-login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('auth/me/', CurrentUserAPIView.as_view(), name='api-current-user'),
    
    # Marketplace endpoints
    path('categories/', CategoryListAPIView.as_view(), name='api-categories'),
    path('items/', RentalItemListAPIView.as_view(), name='api-items'),
    path('items/<uuid:pk>/', RentalItemDetailAPIView.as_view(), name='api-item-detail'),

    # Admin endpoints
    path('admin/users/', AdminUserListAPIView.as_view(), name='api-admin-users'),
    path('admin/verification-requests/', AdminVerificationRequestListAPIView.as_view(), name='api-admin-verification-requests'),
    path('admin/verification-requests/<int:pk>/<str:action>/', AdminVerificationRequestActionAPIView.as_view(), name='api-admin-verification-request-action'),
    path('admin/categories/', AdminCategoryListCreateAPIView.as_view(), name='api-admin-categories'),
    path('admin/categories/<int:pk>/', AdminCategoryRetrieveUpdateDestroyAPIView.as_view(), name='api-admin-category-detail'),
    path('admin/items/', AdminRentalItemListAPIView.as_view(), name='api-admin-items'),
    path('admin/items/<uuid:pk>/', AdminRentalItemRetrieveUpdateAPIView.as_view(), name='api-admin-item-detail'),
    path('admin/bookings/', AdminBookingListAPIView.as_view(), name='api-admin-bookings'),
    path('admin/bookings/<int:pk>/', AdminBookingRetrieveUpdateAPIView.as_view(), name='api-admin-booking-detail'),
]
