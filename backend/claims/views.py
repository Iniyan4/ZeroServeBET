from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notifications.utils import create_notification
from .models import Claim
from .serializers import ClaimSerializer

from food.models import FoodListing
from delivery.models import DeliveryTask
from django.contrib.auth import get_user_model

User = get_user_model()


# 🔥 NGO creates claim
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_claim(request, food_id):
    user = request.user

    # Only NGOs allowed
    if user.role != 'ngo':
        return Response({"error": "Only NGOs can claim food"})

    try:
        food = FoodListing.objects.get(id=food_id)
    except FoodListing.DoesNotExist:
        return Response({"error": "Food not found"})

    # Prevent duplicate claims
    if Claim.objects.filter(food=food, ngo=user).exists():
        return Response({"error": "Already claimed"})

    claim = Claim.objects.create(
        food=food,
        ngo=user,
        notes=request.data.get('notes', '')
    )

    # 🔔 Notify donor
    create_notification(
        user=food.donor,
        title="New Claim Request",
        message=f"{user.username} requested your food",
        notif_type='claim'
    )

    return Response({
        "success": True,
        "message": "Claim submitted",
        "data": ClaimSerializer(claim).data
    })


# 🔥 Donor accepts claim (🔥 MAIN LOGIC)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_claim(request, claim_id):
    print("🔥 ACCEPT CLAIM CALLED")

    try:
        claim = Claim.objects.get(id=claim_id)
        print("✅ Claim found:", claim.id)
    except Claim.DoesNotExist:
        print("❌ Claim not found")
        return Response({"error": "Claim not found"})

    if claim.food.donor != request.user:
        print("❌ Unauthorized user:", request.user.id)
        return Response({"error": "Not authorized"})

    claim.status = 'accepted'
    claim.save()
    print("✅ Claim accepted")

    food = claim.food

    food.status = 'claimed'
    food.save()
    print("✅ Food updated")

    # 🚚 DELIVERY
    from django.contrib.auth import get_user_model
    from delivery.models import DeliveryTask
    User = get_user_model()

    delivery_partner = User.objects.filter(role='delivery').first()
    print("🔍 Delivery partner:", delivery_partner)

    if not delivery_partner:
        print("❌ No delivery partner found")
        return Response({"error": "No delivery partner available"})

    task = DeliveryTask.objects.create(
        claim=claim,
        delivery_partner=delivery_partner,
        pickup_address=food.pickup_address,
        drop_address="NGO Location",
        status="assigned"
    )

    print("🚚 Delivery task created:", task.id)

    # 🔔 NOTIFICATION
    from notifications.utils import create_notification

    create_notification(
        user=delivery_partner,
        title="New Delivery Assigned",
        message=f"Pickup food from {food.donor.username}",
        notif_type='delivery'
    )

    print("🔔 Notification sent")

    return Response({
        "success": True,
        "message": "Claim accepted + delivery created"
    })


# 🔥 Donor rejects claim
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_claim(request, claim_id):
    try:
        claim = Claim.objects.get(id=claim_id)
    except Claim.DoesNotExist:
        return Response({"error": "Claim not found"})

    if claim.food.donor != request.user:
        return Response({"error": "Not authorized"})

    claim.status = 'rejected'
    claim.save()

    return Response({
        "success": True,
        "message": "Claim rejected"
    })


# 🔥 NGO view their claims
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_claims(request):
    claims = Claim.objects.filter(ngo=request.user)

    return Response({
        "success": True,
        "data": ClaimSerializer(claims, many=True).data
    })


# 🔥 Donor view claims on their food
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def food_claims(request, food_id):
    claims = Claim.objects.filter(food_id=food_id)

    return Response({
        "success": True,
        "data": ClaimSerializer(claims, many=True).data
    })