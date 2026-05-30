from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import CustomUserCreationForm, LoginForm, UserProfileForm, UserBasicInfoForm, VerificationUploadForm
from .models import CustomUser, UserProfile, VerificationRequest
from marketplace.models import RentalItem


class SignUpView(CreateView):
    """User registration view"""
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('marketplace:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        # Create user profile
        UserProfile.objects.create(user=user)
        # Log the user in
        login(self.request, user)
        messages.success(self.request, 'Account created successfully! Welcome to RentHub.')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Sign Up'
        return context


def login_view(request):
    """Custom login view with email authentication"""
    if request.user.is_authenticated:
        return redirect('marketplace:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Find user by email
            try:
                user = CustomUser.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    
                    # Redirect to next page if provided
                    next_page = request.POST.get('next') or request.GET.get('next') or 'marketplace:home'
                    return redirect(next_page)
                else:
                    messages.error(request, 'Invalid email or password')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'page_title': 'Login',
    }
    return render(request, 'accounts/login.html', context)


@login_required(login_url='accounts:login')
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('marketplace:home')


@login_required(login_url='accounts:login')
def profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        'profile': profile,
        'page_title': 'My Profile',
        'user_stats': {
            'listings': request.user.rental_items.count(),
            'bookings': request.user.bookings_as_renter.count(),
            'earnings': profile.total_earnings,
        }
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='accounts:login')
def profile_edit_view(request):
    """Edit user profile information"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        user_form = UserBasicInfoForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserBasicInfoForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'page_title': 'Edit Profile',
    }
    return render(request, 'accounts/profile_edit.html', context)


@login_required(login_url='accounts:login')
def dashboard_view(request):
    """User dashboard with stats"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    # Get user statistics
    stats = {
        'total_listings': request.user.rental_items.count(),
        'active_rentals': request.user.rental_items.filter(is_available=True).count(),
        'total_bookings_made': request.user.bookings_as_renter.count(),
        'pending_bookings': request.user.bookings_as_owner.filter(status='pending').count(),
        'total_earnings': profile.total_earnings,
        'average_rating': request.user.overall_rating,
        'total_reviews': request.user.total_reviews,
    }
    
    # Recent bookings
    recent_bookings = request.user.bookings_as_owner.all()[:5]
    
    context = {
        'stats': stats,
        'recent_bookings': recent_bookings,
        'profile': profile,
        'page_title': 'Dashboard',
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='accounts:login')
def verification_upload_view(request):
    """Upload verification document"""
    profile = get_object_or_404(UserProfile, user=request.user)
    verification_request = None
    
    # Check if there's a pending verification
    try:
        verification_request = VerificationRequest.objects.filter(
            user=request.user,
            status='pending'
        ).latest('submitted_at')
    except VerificationRequest.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = VerificationUploadForm(request.POST, request.FILES)
        if form.is_valid():
            verification = VerificationRequest(
                user=request.user,
                document=form.cleaned_data['document'],
                status='pending'
            )
            verification.save()
            messages.success(request, 'Verification document submitted successfully. We will review it shortly.')
            return redirect('accounts:profile')
    else:
        form = VerificationUploadForm()
    
    context = {
        'form': form,
        'profile': profile,
        'verification_request': verification_request,
        'page_title': 'Verify Identity',
        'trust_badges': request.user.trust_badges.all(),
    }
    return render(request, 'accounts/verification_upload.html', context)


def public_profile_view(request, username):
    """View public profile of another user"""
    user = get_object_or_404(CustomUser, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    
    # Get user's listings
    listings = user.rental_items.filter(is_available=True)[:6]
    
    # Get user's reviews
    reviews = user.reviews_received.all()[:5]
    
    context = {
        'profile_user': user,
        'profile': profile,
        'listings': listings,
        'reviews': reviews,
        'page_title': f"{user.first_name}'s Profile",
        'trust_badges': user.trust_badges.all(),
    }
    return render(request, 'accounts/public_profile.html', context)

def verification(request):
    return render(request, 'accounts/verification.html')

def complete_verification(request):
    return render(request, 'accounts/complete_verification.html')