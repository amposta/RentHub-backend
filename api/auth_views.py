from django.contrib.auth import get_user_model, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .auth_serializers import SignupSerializer, LoginSerializer, UserDetailSerializer

User = get_user_model()


@method_decorator(csrf_exempt, name='dispatch')
class SignupAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            user_serializer = UserDetailSerializer(user)
            return Response(
                {'message': 'User registered successfully', 'user': user_serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            user_serializer = UserDetailSerializer(user)
            return Response(
                {'message': 'Logged in successfully', 'user': user_serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(
            {'message': 'Logged out successfully'},
            status=status.HTTP_200_OK,
        )


class CurrentUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            serializer = UserDetailSerializer(request.user)
            return Response({'user': serializer.data}, status=status.HTTP_200_OK)
        return Response({'user': None}, status=status.HTTP_200_OK)
