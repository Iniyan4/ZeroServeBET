from .models import Notification


def create_notification(user, title, message, notif_type='general'):
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notif_type
    )