from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Reliability(models.Model):
    RISK_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reliability')

    completion_rate = models.FloatField(default=100.0)
    cancellation_count = models.IntegerField(default=0)
    no_show_count = models.IntegerField(default=0)
    late_count = models.IntegerField(default=0)
    complaint_count = models.IntegerField(default=0)

    warning_count = models.IntegerField(default=0)
    restriction_count = models.IntegerField(default=0)

    trust_score = models.FloatField(default=100.0)
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES, default='low')

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} | score={self.trust_score} | risk={self.risk_level}"


class Violation(models.Model):
    TYPE_CHOICES = (
        ('fake_listing', 'Fake Listing'),
        ('no_show', 'No Show'),
        ('late', 'Late'),
        ('cancellation', 'Cancellation'),
        ('bad_quality', 'Bad Quality'),
        ('abuse', 'Abuse/Spam'),
    )

    SEVERITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    ACTION_CHOICES = (
        ('warning', 'Warning'),
        ('temp_limit', 'Temporary Limit'),
        ('restricted', 'Restricted'),
        ('review', 'Needs Review'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='violations')
    violation_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    description = models.TextField(blank=True)

    action_taken = models.CharField(max_length=20, choices=ACTION_CHOICES, default='warning')

    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} | {self.violation_type} | {self.severity}"