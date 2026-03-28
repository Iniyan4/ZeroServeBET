from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from reliability.models import Reliability, Violation
from food.models import FoodListing

from services.ai_agent import analyze_user  # your LLM agent

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_review_user(request):

    user_id = request.data.get("user_id")

    try:
        user = User.objects.get(id=user_id)
        rel = Reliability.objects.get(user=user)
        violations = Violation.objects.filter(user=user)

    except Exception as e:
        return Response({
            "success": False,
            "error": "User data not found"
        })

    # Prepare structured data for LLM
    user_data = {
        "trust_score": rel.trust_score,
        "violations": violations.count(),
        "no_show": rel.no_show_count,
        "complaints": rel.complaint_count,
        "risk_level": rel.risk_level
    }

    # 🔥 TRY LLM
    try:
        ai_output = analyze_user(user_data)

        return Response({
            "success": True,
            "source": "llm",
            "data": ai_output
        })

    # 🔒 FALLBACK (VERY IMPORTANT FOR HACKATHON)
    except Exception as e:

        recommendation = "approve"

        if rel.trust_score < 40:
            recommendation = "restrict"
        elif rel.trust_score < 60:
            recommendation = "review"

        return Response({
            "success": True,
            "source": "fallback",
            "data": {
                "summary": f"User has score {rel.trust_score} with {violations.count()} violations",
                "risk_level": rel.risk_level,
                "recommendation": recommendation
            }
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_review_food(request):

    food_id = request.data.get("food_id")

    try:
        food = FoodListing.objects.get(id=food_id)
    except:
        return Response({"error": "Food not found"})

    issues = []

    if food.urgency_score > 85:
        issues.append("High urgency")

    if not food.description:
        issues.append("Missing description")

    if food.quantity <= 0:
        issues.append("Invalid quantity")

    recommendation = "approve"

    if len(issues) >= 2:
        recommendation = "review"

    return Response({
        "success": True,
        "data": {
            "issues": issues,
            "urgency_score": food.urgency_score,
            "recommendation": recommendation
        }
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_complaint_summary(request):

    description = request.data.get("description", "").lower()

    category = "general"
    severity = "low"

    if "late" in description:
        category = "late_delivery"
    elif "bad" in description or "spoiled" in description:
        category = "food_quality"

    if "very" in description or "extremely" in description:
        severity = "high"

    return Response({
        "success": True,
        "data": {
            "category": category,
            "severity": severity,
            "summary": f"Detected {category} issue with {severity} severity"
        }
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_ai_insight(request):

    user_id = request.data.get("user_id")

    try:
        user = User.objects.get(id=user_id)
        rel = Reliability.objects.get(user=user)
        violations = Violation.objects.filter(user=user)

    except:
        return Response({"error": "User not found"})

    user_data = {
        "trust_score": rel.trust_score,
        "violations": violations.count(),
        "no_show": rel.no_show_count,
        "complaints": rel.complaint_count,
        "risk_level": rel.risk_level
    }

    try:
        ai_output = analyze_user(user_data)

        return Response({
            "success": True,
            "ai_summary": ai_output,
            "note": "AI-assisted recommendation. Admin must decide final action."
        })

    except:

        return Response({
            "success": True,
            "ai_summary": f"User has moderate risk with score {rel.trust_score}",
            "note": "Fallback logic used"
        })