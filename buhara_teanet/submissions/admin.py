from django.contrib import admin
from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'submitted_by', 'status', 'location', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('submitted_by__username', 'location', 'notes')