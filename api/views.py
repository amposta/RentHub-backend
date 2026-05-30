from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView

from marketplace.models import Category, RentalItem
from .serializers import CategorySerializer, RentalItemSerializer

User = get_user_model()


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.filter(is_active=True).order_by('display_order', 'name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class RentalItemListAPIView(ListAPIView):
    serializer_class = RentalItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = RentalItem.objects.filter(is_available=True).select_related('category', 'owner')
        category = self.request.query_params.get('category')
        query = self.request.query_params.get('q')
        city = self.request.query_params.get('city')
        condition = self.request.query_params.get('condition')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        sort = self.request.query_params.get('sort', '-created_at')

        if category:
            queryset = queryset.filter(category__slug=category)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )
        if city:
            queryset = queryset.filter(city__icontains=city)
        if condition:
            queryset = queryset.filter(condition=condition)
        if min_price:
            queryset = queryset.filter(price_per_day__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_day__lte=max_price)

        return queryset.order_by(sort)


class RentalItemDetailAPIView(RetrieveAPIView):
    queryset = RentalItem.objects.select_related('category', 'owner').all()
    serializer_class = RentalItemSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'
