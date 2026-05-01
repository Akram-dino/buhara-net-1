from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from accounts.decorators import role_required
from detections.models import DetectionResult
from submissions.models import Submission


@login_required
@role_required(['admin', 'reviewer'])
def analytics_dashboard_view(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status_filter = request.GET.get('status')
    disease_filter = request.GET.get('disease_name')

    submissions = Submission.objects.all()
    detections = DetectionResult.objects.select_related('submission')

    if start_date:
        submissions = submissions.filter(created_at__date__gte=start_date)
        detections = detections.filter(submission__created_at__date__gte=start_date)

    if end_date:
        submissions = submissions.filter(created_at__date__lte=end_date)
        detections = detections.filter(submission__created_at__date__lte=end_date)

    if status_filter:
        submissions = submissions.filter(status=status_filter)
        detections = detections.filter(submission__status=status_filter)

    if disease_filter:
        detections = detections.filter(disease_name=disease_filter)
        submissions = submissions.filter(detection_result__disease_name=disease_filter)

    total_submissions = submissions.count()
    pending_ai = submissions.filter(status='pending_ai').count()
    pending_review = submissions.filter(status='pending_review').count()
    approved = submissions.filter(status='approved').count()
    rejected = submissions.filter(status='rejected').count()
    reviewed = submissions.filter(status='reviewed').count()

    disease_distribution = list(
        detections.values('disease_name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    status_distribution = [
        {'label': 'Pending AI Analysis', 'value': pending_ai},
        {'label': 'Pending Review', 'value': pending_review},
        {'label': 'Approved', 'value': approved},
        {'label': 'Reviewed', 'value': reviewed},
        {'label': 'Rejected', 'value': rejected},
    ]

    recent_submissions = list(
    submissions.select_related('submitted_by').order_by('-created_at')[:10]
)

    for submission in recent_submissions:
            submission.can_delete = (
                request.user.role in ['admin', 'reviewer'] or submission.submitted_by == request.user
            )

    disease_labels = [item['disease_name'] or 'Unknown' for item in disease_distribution]
    disease_values = [item['total'] for item in disease_distribution]

    status_labels = [item['label'] for item in status_distribution]
    status_values = [item['value'] for item in status_distribution]

    available_diseases = (
        DetectionResult.objects.exclude(disease_name__isnull=True)
        .exclude(disease_name__exact='')
        .values_list('disease_name', flat=True)
        .distinct()
        .order_by('disease_name')
    )

    context = {
        'total_submissions': total_submissions,
        'pending_ai': pending_ai,
        'pending_review': pending_review,
        'approved': approved,
        'rejected': rejected,
        'reviewed': reviewed,
        'disease_distribution': disease_distribution,
        'status_distribution': status_distribution,
        'recent_submissions': recent_submissions,
        'disease_labels': disease_labels,
        'disease_values': disease_values,
        'status_labels': status_labels,
        'status_values': status_values,
        'available_diseases': available_diseases,

        # current filters
        'start_date': start_date,
        'end_date': end_date,
        'status_filter': status_filter,
        'disease_filter': disease_filter,
    }

    return render(request, 'analytics_app/dashboard.html', context)