from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from detections.models import DetectionResult
from detections.services import analyze_image_with_roboflow
from .forms import SubmissionForm
from .models import Submission
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Submission

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.decorators import role_required
from detections.models import DetectionResult
from detections.services import analyze_image_with_roboflow
from .forms import SubmissionForm


from .models import Submission




@login_required
@role_required(['worker', 'manager'])
def submission_create_view(request):

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.submitted_by = request.user
            submission.status = 'pending_ai'
            submission.ai_error = None
            submission.save()

            try:
                result = analyze_image_with_roboflow(submission.image.path)

                DetectionResult.objects.update_or_create(
                    submission=submission,
                    defaults={
                        'disease_name': result.get('disease_name'),
                        'confidence': result.get('confidence'),
                        'recommendation': result.get('recommendation'),
                        'raw_response': result.get('raw_response'),
                    }
                )

                submission.status = 'pending_review'
                submission.save()

                messages.success(request, "Submission uploaded and analyzed successfully.")

            except Exception as e:
                submission.status = 'pending_ai'
                submission.ai_error = str(e)
                submission.save()

                messages.warning(request, f"Submission uploaded, but AI failed: {str(e)}")

            return redirect('submission_detail', pk=submission.pk)

    else:
        form = SubmissionForm()   # ✅ THIS WAS MISSING

    # ✅ ALWAYS RETURN THIS
    return render(request, 'submissions/submission_form.html', {
        'form': form
    })


@login_required
@role_required(['worker', 'manager'])
# def submission_list_view(request):
#     submissions = Submission.objects.filter(submitted_by=request.user).order_by('-created_at')
#     return render(request, 'submissions/submission_list.html', {'submissions': submissions})
# @login_required
def submission_list_view(request):
    submissions = Submission.objects.filter(submitted_by=request.user)

    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    if search_query:
        submissions = submissions.filter(
            Q(location__icontains=search_query) |
            Q(notes__icontains=search_query) |
            Q(id__icontains=search_query)
        )

    if status_filter:
        submissions = submissions.filter(status=status_filter)

    submissions = submissions.order_by('-created_at')

    total_records = submissions.count()
    pending_ai = submissions.filter(status='pending_ai').count()
    pending_review = submissions.filter(status='pending_review').count()
    approved = submissions.filter(status='approved').count()

    context = {
        'submissions': submissions,
        'total_records': total_records,
        'pending_ai': pending_ai,
        'pending_review': pending_review,
        'approved': approved,
        'search_query': search_query,
        'status_filter': status_filter,
    }

    return render(request, 'submissions/submission_list.html', context)


@login_required
def submission_detail_view(request, pk):
    submission = get_object_or_404(Submission, pk=pk)

    if request.user.role in ['worker', 'manager'] and submission.submitted_by != request.user:
        messages.error(request, "You are not allowed to view this submission.")
        return redirect('dashboard')

    detection_result = getattr(submission, 'detection_result', None)
    class_scores = []

    if detection_result and detection_result.raw_response:
        predictions = detection_result.raw_response.get('predictions', {})

        if isinstance(predictions, dict):
            for class_name, class_data in predictions.items():
                if isinstance(class_data, dict):
                    confidence = class_data.get('confidence')
                    if confidence is not None:
                        class_scores.append({
                            'name': class_name.replace('_', ' ').title(),
                            'confidence': round(confidence * 100, 2),
                        })

        class_scores = sorted(
            class_scores,
            key=lambda x: x['confidence'],
            reverse=True
        )[:5]

    context = {
        'submission': submission,
        'class_scores': class_scores,
    }
    return render(request, 'submissions/submission_detail.html', context)


@login_required
def submission_delete_view(request, pk):
    submission = get_object_or_404(Submission, pk=pk)

    if request.user.role in ['worker', 'manager'] and submission.submitted_by != request.user:
        messages.error(request, "You are not allowed to delete this submission.")
        return redirect('dashboard')

    if request.method == 'POST':
        next_url = request.POST.get('next')
        submission.delete()
        messages.success(request, "Submission deleted successfully.")

        if next_url:
            return redirect(next_url)

        if request.user.role in ['admin', 'reviewer']:
            return redirect('analytics_dashboard')

        return redirect('submission_list')

    return redirect('submission_detail', pk=pk)


@login_required
@role_required(['worker', 'manager'])
def submission_update_view(request, pk):
    submission = get_object_or_404(Submission, pk=pk, submitted_by=request.user)

    # Optional restriction: prevent editing after approval/review
    if submission.status in ['approved', 'reviewed', 'rejected']:
        messages.error(request, "You cannot edit a submission that has already been reviewed.")
        return redirect('submission_detail', pk=submission.pk)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            updated_submission = form.save(commit=False)

            # If worker changes the image/details, reset workflow
            updated_submission.status = 'pending_ai'
            updated_submission.ai_error = None
            updated_submission.save()

            # remove old detection result if it exists
            detection_result = getattr(updated_submission, 'detection_result', None)
            if detection_result:
                detection_result.delete()

            try:
                result = analyze_image_with_roboflow(updated_submission.image.path)

                DetectionResult.objects.update_or_create(
                    submission=updated_submission,
                    defaults={
                        'disease_name': result.get('disease_name'),
                        'confidence': result.get('confidence'),
                        'recommendation': result.get('recommendation'),
                        'raw_response': result.get('raw_response'),
                    }
                )

                updated_submission.status = 'pending_review'
                updated_submission.ai_error = None
                updated_submission.save()

                messages.success(request, "Submission updated and re-analyzed successfully.")
            except Exception as e:
                updated_submission.status = 'pending_ai'
                updated_submission.ai_error = str(e)
                updated_submission.save()
                messages.warning(request, f"Submission updated, but AI analysis failed: {str(e)}")

            return redirect('submission_detail', pk=updated_submission.pk)
    else:
        form = SubmissionForm(instance=submission)

    return render(request, 'submissions/submission_form.html', {
        'form': form,
        'is_edit': True,
        'submission': submission,
    })





@login_required
@role_required(['worker', 'manager'])
def submission_update_view(request, pk):
    submission = get_object_or_404(Submission, pk=pk, submitted_by=request.user)

    # Optional restriction: prevent editing after approval/review
    if submission.status in ['approved', 'reviewed', 'rejected']:
        messages.error(request, "You cannot edit a submission that has already been reviewed.")
        return redirect('submission_detail', pk=submission.pk)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            updated_submission = form.save(commit=False)

            # If worker changes the image/details, reset workflow
            updated_submission.status = 'pending_ai'
            updated_submission.ai_error = None
            updated_submission.save()

            # remove old detection result if it exists
            detection_result = getattr(updated_submission, 'detection_result', None)
            if detection_result:
                detection_result.delete()

            try:
                result = analyze_image_with_roboflow(updated_submission.image.path)

                DetectionResult.objects.update_or_create(
                    submission=updated_submission,
                    defaults={
                        'disease_name': result.get('disease_name'),
                        'confidence': result.get('confidence'),
                        'recommendation': result.get('recommendation'),
                        'raw_response': result.get('raw_response'),
                    }
                )

                updated_submission.status = 'pending_review'
                updated_submission.ai_error = None
                updated_submission.save()

                messages.success(request, "Submission updated and re-analyzed successfully.")
            except Exception as e:
                updated_submission.status = 'pending_ai'
                updated_submission.ai_error = str(e)
                updated_submission.save()
                messages.warning(request, f"Submission updated, but AI analysis failed: {str(e)}")

            return redirect('submission_detail', pk=updated_submission.pk)
    else:
        form = SubmissionForm(instance=submission)

    return render(request, 'submissions/submission_form.html', {
        'form': form,
        'is_edit': True,
        'submission': submission,
    })