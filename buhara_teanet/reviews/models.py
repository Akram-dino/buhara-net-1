from django.conf import settings
from django.db import models
from submissions.models import Submission


class Review(models.Model):
    REVIEW_STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('corrected', 'Corrected'),
        ('rejected', 'Rejected'),
    ]

    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name='review'
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    final_disease_name = models.CharField(max_length=255)
    final_recommendation = models.TextField()
    expert_notes = models.TextField(blank=True, null=True)
    review_status = models.CharField(max_length=20, choices=REVIEW_STATUS_CHOICES)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Submission #{self.submission.id}"