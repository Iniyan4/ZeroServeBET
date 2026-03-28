from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notifications.utils import create_notification
from .models import Claim
from .serializers import ClaimSerializer

from food.models import FoodListing


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

    # Check if already claimed
    if Claim.objects.filter(food=food, ngo=user).exists():
        return Response({"error": "Already claimed"})

    claim = Claim.objects.create(
        food=food,
        ngo=user,
        notes=request.data.get('notes')
    )

    create_notification(
        user=food.donor,
        title="New Claim Request",
        message=f"{request.user.username} requested your food",
        notif_type='claim'
    )

    return Response({
        "success": True,
        "message": "Claim submitted",
        "data": ClaimSerializer(claim).data
    })


# 🔥 Donor accepts claim
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_claim(request, claim_id):
    try:
        claim = Claim.objects.get(id=claim_id)
    except Claim.DoesNotExist:
        return Response({"error": "Claim not found"})

    # Only donor can accept
    if claim.food.donor != request.user:
        return Response({"error": "Not authorized"})

    claim.status = 'accepted'
    claim.save()

    create_notification(
        user=claim.ngo,
        title="Claim Accepted",
        message="Your claim has been accepted",
        notif_type='claim'
    )

    # Update food status
    claim.food.status = 'claimed'
    claim.food.save()

    return Response({
        "success": True,
        "message": "Claim accepted"
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