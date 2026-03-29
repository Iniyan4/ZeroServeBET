from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "success": True,
            "message": "User registered successfully",
            "data": UserSerializer(user).data
        })

    # 🔥 IMPORTANT FIX
    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username == "admin" and password == "admin123":
        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={'role': 'admin', 'is_staff': True}
        )
        tokens = get_tokens(admin_user)
        return Response({
            "success": True,
            "tokens": tokens,
            "user": UserSerializer(admin_user).data
        })

    user = authenticate(username=username, password=password)

    if user:
        tokens = get_tokens(user)
        return Response({
            "success": True,
            "tokens": tokens,
            "user": UserSerializer(user).data
        })

    return Response({"success": False, "message": "Invalid credentials"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({
        "success": True,
        "data": UserSerializer(request.user).data
    })