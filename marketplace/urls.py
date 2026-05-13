from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    # Public views
    path('', views.homepage, name='home'),
    path('explore/', views.explore, name='explore'),
    path('item/<uuid:item_id>/', views.listing_detail, name='listing_detail'),
    
    # Wishlist
    path('item/<uuid:item_id>/wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    
    # User's listings
    path('listings/', views.RentalItemListView.as_view(), name='my_listings'),
    path('item/create/', views.RentalItemCreateView.as_view(), name='item_create'),
    path('item/<uuid:pk>/edit/', views.RentalItemUpdateView.as_view(), name='item_edit'),
    path('item/<uuid:pk>/delete/', views.RentalItemDeleteView.as_view(), name='item_delete'),
]