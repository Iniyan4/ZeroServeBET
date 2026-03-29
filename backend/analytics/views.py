from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from food.models import FoodListing
from delivery.models import DeliveryTask
from claims.models import Claim
from services.ai_agent import analyze_user


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_analytics(request):

    total_food = FoodListing.objects.count()
    total_delivered = FoodListing.objects.filter(status='delivered').count()
    total_claims = Claim.objects.count()

    return Response({
        "success": True,
        "data": {
            "total_food_listings": total_food,
            "total_delivered": total_delivered,
            "total_claims": total_claims,
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def donor_analytics(request):

    user = request.user

    foods = FoodListing.objects.filter(donor=user)

    total_donated = foods.count()
    total_servings = sum(f.servings for f in foods)
    delivered = foods.filter(status='delivered').count()

    return Response({
        "success": True,
        "data": {
            "total_donations": total_donated,
            "total_servings": total_servings,
            "delivered_count": delivered,
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ngo_analytics(request):

    user = request.user

    claims = Claim.objects.filter(ngo=user)

    total_claims = claims.count()
    accepted = claims.filter(status='accepted').count()
    completed = claims.filter(status='completed').count()

    return Response({
        "success": True,
        "data": {
            "total_claims": total_claims,
            "accepted": accepted,
            "completed": completed,
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delivery_analytics(request):

    user = request.user

    tasks = DeliveryTask.objects.filter(delivery_partner=user)

    total_tasks = tasks.count()
    completed = tasks.filter(status='delivered').count()
    failed = tasks.filter(status='failed').count()

    return Response({
        "success": True,
        "data": {
            "total_tasks": total_tasks,
            "completed": completed,
            "failed": failed,
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def impact_metrics(request):

    delivered_food = FoodListing.objects.filter(status='delivered')

    total_servings = sum(f.servings for f in delivered_food)

    return Response({
        "success": True,
        "data": {
            "total_meals_saved": total_servings,
            "food_waste_reduced": total_servings,  # same metric for demo
        }
    })

@api_view(['GET'])
def admin_ngo_detail(request, ngo_id):
    from accounts.models import User
    from claims.models import Claim
    from delivery.models import DeliveryTask

    ngo = User.objects.get(id=ngo_id)

    claims = Claim.objects.filter(ngo=ngo)
    deliveries = DeliveryTask.objects.filter(claim__ngo=ngo)

    donors = list(set([c.food.donor.username for c in claims]))

    return Response({
        "ngo": ngo.username,
        "total_claims": claims.count(),
        "deliveries_completed": deliveries.filter(status='delivered').count(),
        "donors_served": donors
    })

@api_view(['GET'])
def admin_donor_detail(request, donor_id):
    from accounts.models import User
    from food.models import FoodListing

    donor = User.objects.get(id=donor_id)
    foods = FoodListing.objects.filter(donor=donor)

    ngos = list(set([
        f.claim_set.first().ngo.username
        for f in foods if f.claim_set.exists()
    ]))

    return Response({
        "donor": donor.username,
        "total_food": foods.count(),
        "total_servings": sum(f.servings for f in foods),
        "ngos_served": ngos
    })

@api_view(['GET'])
def admin_delivery_detail(request, partner_id):
    from accounts.models import User
    from delivery.models import DeliveryTask

    partner = User.objects.get(id=partner_id)
    tasks = DeliveryTask.objects.filter(delivery_partner=partner)

    return Response({
        "partner": partner.username,
        "total_tasks": tasks.count(),
        "completed": tasks.filter(status='delivered').count(),
        "failed": tasks.filter(status='failed').count()
    })

@api_view(['POST'])
def admin_ai_insight(request):
    entity_type = request.data.get("type")  # donor / ngo / delivery
    user_id = request.data.get("user_id")

    # fetch reliability + performance data

    # pass to AI agent
    ai_output = analyze_user(request.data)

    return Response({
        "success": True,
        "ai_summary": ai_output
    })