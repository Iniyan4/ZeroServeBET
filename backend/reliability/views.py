from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Reliability, Violation
from .serializers import ReliabilitySerializer, ViolationSerializer

from services.reliability_engine import (
    compute_trust_score,
    compute_risk_level,
    decide_action
)

User = get_user_model()


def _get_or_create_rel(user):
    rel, _ = Reliability.objects.get_or_create(user=user)
    return rel


# 🔥 Get reliability for a user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reliability(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"})

    rel = _get_or_create_rel(user)
    return Response({
        "success": True,
        "data": ReliabilitySerializer(rel).data
    })


# 🔥 Add violation (called from complaints/admin/automation)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_violation(request):
    user_id = request.data.get('user_id')
    vtype = request.data.get('violation_type')
    severity = request.data.get('severity', 'low')
    description = request.data.get('description', '')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"})

    rel = _get_or_create_rel(user)

    action = decide_action(severity, rel.warning_count)

    v = Violation.objects.create(
        user=user,
        violation_type=vtype,
        severity=severity,
        description=description,
        action_taken=action
    )

    # Update counters based on type
    if vtype == 'no_show':
        rel.no_show_count += 1
    elif vtype == 'late':
        rel.late_count += 1
    elif vtype == 'cancellation':
        rel.cancellation_count += 1
    elif vtype == 'bad_quality':
        rel.complaint_count += 1

    # Apply action effects
    if action == 'warning':
        rel.warning_count += 1

    elif action == 'temp_limit':
        rel.warning_count += 1
        # You can enforce temp limits in permission checks

    elif action == 'restricted':
        rel.restriction_count += 1
        user.is_restricted = True
        user.save()

    # Recompute score + risk
    rel.trust_score = compute_trust_score({
        "completion_rate": rel.completion_rate,
        "cancellation_count": rel.cancellation_count,
        "no_show_count": rel.no_show_count,
        "late_count": rel.late_count,
        "complaint_count": rel.complaint_count,
    })
    rel.risk_level = compute_risk_level(rel.trust_score)

    rel.save()

    return Response({
        "success": True,
        "message": f"Violation recorded ({action})",
        "data": {
            "violation": ViolationSerializer(v).data,
            "reliability": ReliabilitySerializer(rel).data
        }
    })


# 🔥 Admin: restrict/unrestrict user explicitly
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_restriction(request):
    # simple admin check (you can tighten this)
    if request.user.role != 'admin':
        return Response({"error": "Admin only"})

    user_id = request.data.get('user_id')
    restrict = request.data.get('restrict', True)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"})

    user.is_restricted = bool(restrict)
    user.save()

    rel = _get_or_create_rel(user)
    if restrict:
        rel.restriction_count += 1
    rel.save()

    return Response({
        "success": True,
        "message": f"User {'restricted' if restrict else 'unrestricted'}"
    })


# 🔥 List violations for a user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_violations(request, user_id):
    qs = Violation.objects.filter(user_id=user_id).order_by('-created_at')
    return Response({
        "success": True,
        "data": ViolationSerializer(qs, many=True).data
    })