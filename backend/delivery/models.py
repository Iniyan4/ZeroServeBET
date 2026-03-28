from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class DeliveryTask(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('accepted', 'Accepted'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    )

    claim = models.ForeignKey('claims.Claim', on_delete=models.CASCADE)
    delivery_partner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    pickup_address = models.TextField()
    drop_address = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    assigned_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery {self.id} - {self.status}"