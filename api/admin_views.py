from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    AdminUserSerializer,
    AdminVerificationRequestSerializer,
    AdminCategorySerializer,
    AdminRentalItemSerializer,
    AdminBookingSerializer,
)
from accounts.models import VerificationRequest
from bookings.models import Booking
from marketplace.models import Category, RentalItem

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class AdminUserListAPIView(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.order_by('-date_joined')
    serializer_class = AdminUserSerializer

@method_decorator(csrf_exempt, name='dispatch')
class AdminVerificationRequestListAPIView(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = VerificationRequest.objects.select_related('user', 'reviewed_by').order_by('-submitted_at')
    serializer_class = AdminVerificationRequestSerializer

@method_decorator(csrf_exempt, name='dispatch')
class AdminVerificationRequestActionAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk, action):
        verification_request = get_object_or_404(VerificationRequest, pk=pk)

        if action == 'approve':
            verification_request.status = 'approved'
        elif action == 'reject':
            verification_request.status = 'rejected'
        else:
            return Response({'detail': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        verification_request.reviewed_by = request.user
        verification_request.reviewed_at = timezone.now()
        verification_request.save()

        serializer = AdminVerificationRequestSerializer(verification_request)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class AdminCategoryListCreateAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.order_by('display_order', 'name')
    serializer_class = AdminCategorySerializer

@method_decorator(csrf_exempt, name='dispatch')
class AdminCategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.order_by('display_order', 'name')
    serializer_class = AdminCategorySerializer

@method_decorator(csrf_exempt, name='dispatch')
class AdminRentalItemListAPIView(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = RentalItem.objects.select_related('category', 'owner').order_by('-created_at')
    serializer_class = AdminRentalItemSerializer

@method_decorator(csrf_exempt, name='dispatch')
class AdminRentalItemRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = RentalItem.objects.select_related('category', 'owner').all()
    serializer_class = AdminRentalItemSerializer
    lookup_field = 'id'

@method_decorator(csrf_exempt, name='dispatch')
class AdminBookingListAPIView(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Booking.objects.select_related('renter', 'owner', 'item').order_by('-created_at')
    serializer_class = AdminBookingSerializer

@method_decorator(csrf_exempt, name='dispatch')
class AdminBookingRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Booking.objects.select_related('renter', 'owner', 'item').all()
    serializer_class = AdminBookingSerializer
