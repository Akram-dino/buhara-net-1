from django.conf import settings
from django.db import models


from django.conf import settings
from django.db import models


class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending_ai', 'Pending AI Analysis'),
        ('pending_review', 'Pending Review'),
        ('approved', 'Approved'),
        ('reviewed', 'Reviewed'),
        ('rejected', 'Rejected'),
    ]

    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    image = models.ImageField(upload_to='submissions/')
    location = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_ai')
    ai_error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def location_label(self):
        if self.location:
            return self.location
        if self.latitude is not None and self.longitude is not None:
            return f"{self.latitude}, {self.longitude}"
        return "Not specified"

    def __str__(self):
        return f"Submission #{self.id}"