from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.utils import timezone

from notifications.utils import create_notification
from .models import DeliveryTask
from .serializers import DeliverySerializer

from claims.models import Claim


# 🔥 Create delivery after claim accepted
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_delivery(request, claim_id):
    try:
        claim = Claim.objects.get(id=claim_id, status='accepted')
    except Claim.DoesNotExist:
        return Response({"error": "Invalid claim"})

    # Only donor can trigger
    if claim.food.donor != request.user:
        return Response({"error": "Not authorized"})

    delivery = DeliveryTask.objects.create(
        claim=claim,
        pickup_address=claim.food.pickup_address,
        drop_address="NGO Location"  # you can expand later
    )

    return Response({
        "success": True,
        "message": "Delivery created",
        "data": DeliverySerializer(delivery).data
    })


# 🔥 Assign delivery partner
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_partner(request, task_id):
    try:
        task = DeliveryTask.objects.get(id=task_id)
    except DeliveryTask.DoesNotExist:
        return Response({"error": "Task not found"})

    partner_id = request.data.get('partner_id')

    task.delivery_partner_id = partner_id
    task.status = 'assigned'
    task.assigned_at = timezone.now()
    task.save()

    create_notification(
        user=task.delivery_partner,
        title="New Delivery Assigned",
        message="You have a new delivery task",
        notif_type='delivery'
    )

    return Response({
        "success": True,
        "message": "Partner assigned"
    })


# 🔥 Delivery partner accepts task
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_delivery(request, task_id):
    try:
        task = DeliveryTask.objects.get(id=task_id)
    except:
        return Response({"error": "Task not found"})

    if request.user.role != 'delivery':
        return Response({"error": "Only delivery partners allowed"})

    task.delivery_partner = request.user
    task.status = 'accepted'
    task.save()

    create_notification(
        user=task.claim.food.donor,
        title="Delivery Completed",
        message="Your food has been delivered",
        notif_type='delivery'
    )

    return Response({
        "success": True,
        "message": "Task accepted"
    })


# 🔥 Update delivery status
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_status(request, task_id):
    try:
        task = DeliveryTask.objects.get(id=task_id)
    except:
        return Response({"error": "Task not found"})

    status = request.data.get('status')

    if status not in ['picked_up', 'in_transit', 'delivered']:
        return Response({"error": "Invalid status"})

    task.status = status

    if status == 'picked_up':
        task.picked_up_at = timezone.now()

    if status == 'delivered':
        task.delivered_at = timezone.now()

        # 🔥 mark food delivered
        task.claim.food.status = 'delivered'
        task.claim.food.save()

    task.save()

    return Response({
        "success": True,
        "message": f"Updated to {status}"
    })


# 🔥 Get my tasks (delivery partner)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tasks(request):
    if request.user.role != 'delivery':
        return Response({"error": "Not allowed"})

    tasks = DeliveryTask.objects.filter(delivery_partner=request.user)

    return Response({
        "success": True,
        "data": DeliverySerializer(tasks, many=True).data
    })


# 🔥 Get delivery details
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delivery_detail(request, task_id):
    try:
        task = DeliveryTask.objects.get(id=task_id)
    except:
        return Response({"error": "Not found"})

    return Response({
        "success": True,
        "data": DeliverySerializer(task).data
    })