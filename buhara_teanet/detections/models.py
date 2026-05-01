from django.db import models
from submissions.models import Submission


class DetectionResult(models.Model):
    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name='detection_result'
    )
    disease_name = models.CharField(max_length=255, blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    raw_response = models.JSONField(blank=True, null=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    @property
    def has_confidence(self):
        return self.confidence is not None

    @property
    def confidence_percent(self):
        if self.confidence is None:
            return None
        return round(self.confidence * 100, 2)

    def __str__(self):
        return f"Detection for Submission #{self.submission.id}"