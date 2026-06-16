from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Category, RentalItem, Wishlist
from bookings.models import Booking


def homepage(request):
    """Homepage with hero, categories, trending, and near you sections"""
    
    # Get all active categories
    categories = Category.objects.filter(is_active=True).order_by('display_order')
    
    # Get trending rentals (most booked)
    trending_rentals = RentalItem.objects.filter(
        is_available=True
    ).annotate(
        avg_rating=Avg('bookings__review__rating')
    ).order_by('-total_bookings')[:4]
    
    # Get items near user (for now, just get random active items)
    near_you = RentalItem.objects.filter(is_available=True).order_by('-created_at')[:8]
    
    # Get hero slides data
    hero_slides = [
        {
            'title': 'Rent More, Pay Less.',
            'subtitle': 'Rent what you need. Save more. From everyday items to big adventures.',
            'button_text': 'Explore Now',
            'image': 'images/hero-1.jpg'
        },
        {
            'title': 'Quality & Trust',
            'subtitle': 'Every item is verified. Every host is trusted. Shop with confidence.',
            'button_text': 'Browse Items',
            'image': 'images/hero-2.jpg'
        },
    ]
    
    context = {
        'categories': categories,
        'trending_rentals': trending_rentals,
        'near_you': near_you,
        'hero_slides': hero_slides,
        'page_title': 'RentHub - Rent Anything',
    }
    return render(request, 'marketplace/homepage.html', context)


def explore(request):
    """Browse and filter rental items"""
    
    # Get all items
    items = RentalItem.objects.filter(is_available=True)
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        items = items.filter(category__slug=category_slug)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        items = items.filter(price_per_day__gte=min_price)
    if max_price:
        items = items.filter(price_per_day__lte=max_price)
    
    # Filter by search query
    search_query = request.GET.get('q')
    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Filter by condition
    condition = request.GET.get('condition')
    if condition:
        items = items.filter(condition=condition)
    
    # Filter by city
    city = request.GET.get('city')
    if city:
        items = items.filter(city__icontains=city)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    items = items.order_by(sort_by)
    
    # Get all categories for filter sidebar
    categories = Category.objects.filter(is_active=True).order_by('display_order')
    
    context = {
        'items': items,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
        'page_title': 'Explore Rentals',
    }
    return render(request, 'marketplace/explore.html', context)


def listing_detail(request, item_id):
    """Detailed view of a single rental item"""
    
    item = get_object_or_404(RentalItem, id=item_id)
    errors = []
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        if not request.user.can_rent:
            messages.error(request, 'You must complete identity verification before renting an item.')
            return redirect('accounts:verification')

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        special_requests = request.POST.get('special_requests', '').strip()

        if not start_date or not end_date:
            errors.append('Please select both pickup and dropoff dates.')
        else:
            start_date_obj = parse_date(start_date)
            end_date_obj = parse_date(end_date)
            if not start_date_obj or not end_date_obj:
                errors.append('One or more dates are invalid.')
            elif start_date_obj > end_date_obj:
                errors.append('Dropoff date must be after pickup date.')

        if not errors:
            Booking.objects.create(
                renter=request.user,
                item=item,
                owner=item.owner,
                start_date=start_date_obj,
                end_date=end_date_obj,
                special_requests=special_requests,
            )
            messages.success(request, 'Booking requested successfully. Check your Dropoff page for details.')
            return redirect('marketplace:dropoff')
    
    # Get owner info
    owner = item.owner
    owner_ratings = owner.reviews_received.all()
    avg_owner_rating = owner.overall_rating if hasattr(owner, 'overall_rating') else 0
    
    # Get images
    images = item.get_images()
    
    # Get reviews for this item
    reviews = item.bookings.filter(review__isnull=False).select_related('review').order_by('-review__created_at')[:5]
    
    # Check if user has this in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, item=item).exists()
    
    # Get related items from same category
    related_items = RentalItem.objects.filter(
        category=item.category,
        is_available=True
    ).exclude(id=item.id)[:6]
    
    context = {
        'item': item,
        'owner': owner,
        'avg_owner_rating': avg_owner_rating,
        'total_owner_reviews': owner_ratings.count(),
        'images': images,
        'reviews': reviews,
        'in_wishlist': in_wishlist,
        'related_items': related_items,
        'errors': errors,
        'page_title': item.title,
    }
    
    return render(request, 'marketplace/listing_detail.html', context)


class RentalItemListView(LoginRequiredMixin, ListView):
    """List view for user's own rental items"""
    model = RentalItem
    template_name = 'marketplace/my_listings.html'
    context_object_name = 'items'
    paginate_by = 12
    
    def get_queryset(self):
        return RentalItem.objects.filter(owner=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Listings'
        context['total_items'] = self.get_queryset().count()
        return context


class RentalItemCreateView(LoginRequiredMixin, CreateView):
    """Create a new rental item"""
    login_url = 'accounts:login'
    redirect_field_name = 'next'
    model = RentalItem
    template_name = 'marketplace/item_form.html'
    fields = ['category', 'title', 'description', 'price_per_day', 'security_deposit', 'dynamic_attributes', 'location', 'city', 'state', 
              'condition', 'image1', 'image2', 'image3', 'image4', 'image5']
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.can_list_items:
            messages.error(request, 'You must complete identity verification and payout onboarding before listing an item.')
            return redirect('accounts:owner_onboarding')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Item listed successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('marketplace:my_listings')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'List New Item'
        return context


class RentalItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update a rental item (owner only)"""
    model = RentalItem
    template_name = 'marketplace/item_form.html'
    fields = ['category', 'title', 'description', 'price_per_day', 'location', 'city', 'state',
              'condition', 'is_available', 'image1', 'image2', 'image3', 'image4', 'image5']
    
    def test_func(self):
        item = self.get_object()
        return item.owner == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Item updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('marketplace:my_listings')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit Item'
        return context


class RentalItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a rental item (owner only)"""
    model = RentalItem
    template_name = 'marketplace/item_confirm_delete.html'
    success_url = reverse_lazy('marketplace:my_listings')
    
    def test_func(self):
        item = self.get_object()
        return item.owner == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Item deleted successfully!')
        return super().delete(request, *args, **kwargs)


@login_required
@require_POST
def toggle_wishlist(request, item_id):
    """Add/remove item from wishlist (AJAX)"""
    item = get_object_or_404(RentalItem, id=item_id)
    
    wishlist_entry, created = Wishlist.objects.get_or_create(
        user=request.user,
        item=item
    )
    
    if not created:
        wishlist_entry.delete()
        return JsonResponse({'status': 'removed'})
    
    return JsonResponse({'status': 'added'})


@login_required
def wishlist_view(request):
    """View user's saved items"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('item').order_by('-added_at')
    
    context = {
        'wishlist_items': wishlist_items,
        'page_title': 'My Wishlist',
    }
    return render(request, 'marketplace/wishlist.html', context)


@login_required(login_url='accounts:login')
def dropoff_view(request):
    """Dropoff page showing current bookings and dropoff details."""
    bookings = Booking.objects.filter(renter=request.user).order_by('-created_at')
    context = {
        'bookings': bookings,
        'page_title': 'Dropoff',
    }
    return render(request, 'marketplace/dropoff.html', context)