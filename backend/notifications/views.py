from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


# 🔥 Get my notifications
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    return Response({
        "success": True,
        "data": NotificationSerializer(notifications, many=True).data
    })


# 🔥 Mark as read
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_read(request, notif_id):
    try:
        notif = Notification.objects.get(id=notif_id, user=request.user)
    except:
        return Response({"error": "Not found"})

    notif.is_read = True
    notif.save()

    return Response({
        "success": True,
        "message": "Marked as read"
    })