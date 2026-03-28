from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class FoodListing(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('claimed', 'Claimed'),
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    )

    donor = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    food_category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    servings = models.IntegerField()

    is_veg = models.BooleanField(default=True)

    prepared_at = models.DateTimeField()
    expiry_time = models.DateTimeField(null=True, blank=True)

    pickup_address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    urgency_score = models.FloatField(default=0)
    quality_risk = models.CharField(max_length=20, default='low')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title