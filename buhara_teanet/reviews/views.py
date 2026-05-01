from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from submissions.models import Submission
from .forms import ReviewForm
from .models import Review


@login_required
@role_required(['reviewer', 'admin'])
def reviewer_submission_list_view(request):
    submissions = Submission.objects.filter(status='pending_review').order_by('-created_at')
    return render(request, 'reviews/reviewer_submission_list.html', {
        'submissions': submissions
    })


@login_required
@role_required(['reviewer', 'admin'])
def reviewer_submission_detail_view(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    detection_result = getattr(submission, 'detection_result', None)
    existing_review = getattr(submission, 'review', None)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.submission = submission
            review.reviewer = request.user
            review.save()

            if review.review_status == 'approved':
                submission.status = 'approved'
            elif review.review_status == 'rejected':
                submission.status = 'rejected'
            elif review.review_status == 'corrected':
                submission.status = 'reviewed'

            submission.save()

            messages.success(request, "Review submitted successfully.")
            return redirect('reviewer_submission_list')
    else:
        initial_data = {}

        if detection_result:
            initial_data = {
                'final_disease_name': detection_result.disease_name,
                'final_recommendation': detection_result.recommendation,
            }

        form = ReviewForm(instance=existing_review, initial=initial_data)

    return render(request, 'reviews/reviewer_submission_detail.html', {
        'submission': submission,
        'detection_result': detection_result,
        'review': existing_review,
        'form': form,
    })