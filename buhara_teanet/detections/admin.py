from django.contrib import admin
from .models import DetectionResult


@admin.register(DetectionResult)
class DetectionResultAdmin(admin.ModelAdmin):
    list_display = ('submission', 'disease_name', 'confidence', 'analyzed_at')
    search_fields = ('disease_name', 'submission__id')