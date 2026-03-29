from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notifications.utils import create_notification
from .models import FoodListing
from .serializers import FoodSerializer

from services.expiry_engine import calculate_expiry
from services.urgency_engine import calculate_urgency


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_food(request):
    data = request.data

    serializer = FoodSerializer(data=data)

    if serializer.is_valid():
        food = serializer.save(donor=request.user)

        # 🔥 Apply smart logic
        food.expiry_time = calculate_expiry(
            food.food_category,
            food.prepared_at
        )

        food.urgency_score = calculate_urgency(
            food.expiry_time,
            food.quantity
        )

    if food.urgency_score > 85:
    # send to nearby NGOs (simplified)
        from django.contrib.auth import get_user_model
        User = get_user_model()

        ngos = User.objects.filter(role='ngo')

        for ngo in ngos:
            create_notification(
                user=ngo,
                title="URGENT FOOD AVAILABLE",
                message=f"{food.title} needs immediate pickup!",
                notif_type='urgent'
            )

        food.save()

        return Response({
            "success": True,
            "message": "Food created successfully",
            "data": FoodSerializer(food).data
        })

    return Response(serializer.errors)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_food(request):
    foods = FoodListing.objects.filter(status='available')

    serializer = FoodSerializer(foods, many=True)

    return Response({
        "success": True,
        "data": serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def food_detail(request, food_id):
    try:
        food = FoodListing.objects.get(id=food_id)
    except FoodListing.DoesNotExist:
        return Response({"error": "Not found"})

    return Response({
        "success": True,
        "data": FoodSerializer(food).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_food(request, food_id):
    try:
        food = FoodListing.objects.get(id=food_id, donor=request.user)
    except:
        return Response({"error": "Not allowed"})

    food.status = 'cancelled'
    food.save()

    return Response({
        "success": True,
        "message": "Cancelled successfully"
    })