from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('submission', 'reviewer', 'review_status', 'reviewed_at')
    list_filter = ('review_status', 'reviewed_at')
    search_fields = ('submission__id', 'final_disease_name', 'reviewer__username')