from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<str:username>/', views.public_profile_view, name='public_profile'),
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path('verification/', views.verification_upload_view, name='verification'),
    path('owner/onboarding/', views.owner_onboarding_view, name='owner_onboarding'),
]