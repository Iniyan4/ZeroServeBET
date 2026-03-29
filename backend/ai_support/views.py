from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from claims.models import Claim
from delivery.models import DeliveryTask

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_insights(request):
    if request.user.role != 'admin':
        return Response({"error": "Unauthorized"}, status=403)

    insights = []

    # 1. Analyze NGOs (Check for rejected claims by Donors)
    ngos = User.objects.filter(role='ngo')
    for ngo in ngos:
        rejections = Claim.objects.filter(ngo=ngo, status='rejected').count()
        if rejections > 0:
            risk = 'critical' if rejections >= 3 else ('high' if rejections == 2 else 'medium')
            action = 'restrict' if rejections >= 3 else 'review'
            insights.append({
                "user_id": ngo.id,
                "username": ngo.username,
                "role": "ngo",
                "risk_classification": risk,
                "ai_summary": f"This NGO has had {rejections} claim(s) explicitly rejected by Donors. This indicates potential unreliability or misuse of the platform.",
                "suggested_action": action
            })

    # 2. Analyze Delivery Partners (Check for disputed deliveries by NGOs)
    partners = User.objects.filter(role='delivery')
    for partner in partners:
        # Find tasks assigned to this partner where the related claim was disputed by the NGO
        disputes = DeliveryTask.objects.filter(delivery_partner=partner, claim__status='disputed').count()
        if disputes > 0:
            risk = 'critical' if disputes >= 2 else 'high'
            action = 'restrict' if disputes >= 2 else 'review'
            insights.append({
                "user_id": partner.id,
                "username": partner.username,
                "role": "delivery",
                "risk_classification": risk,
                "ai_summary": f"This partner has been disputed {disputes} time(s) by NGOs for failing to deliver food properly or faking a delivery status.",
                "suggested_action": action
            })

    return Response({"success": True, "data": insights})