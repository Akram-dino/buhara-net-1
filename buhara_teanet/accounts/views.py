from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .decorators import role_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import role_required
from .forms import AdminUserCreationForm, AdminUserUpdateForm
from .models import User

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .decorators import role_required
from submissions.models import Submission


@login_required
@role_required(['worker', 'manager'])
def worker_dashboard_view(request):
    submissions = Submission.objects.filter(submitted_by=request.user)

    total_submissions = submissions.count()
    pending_ai = submissions.filter(status='pending_ai').count()
    pending_review = submissions.filter(status='pending_review').count()
    approved = submissions.filter(status='approved').count()
    rejected = submissions.filter(status='rejected').count()
    reviewed = submissions.filter(status='reviewed').count()

    recent_submissions = submissions.order_by('-created_at')[:5]

    context = {
        'total_submissions': total_submissions,
        'pending_ai': pending_ai,
        'pending_review': pending_review,
        'approved': approved,
        'rejected': rejected,
        'reviewed': reviewed,
        'recent_submissions': recent_submissions,
    }

    return render(request, 'accounts/worker_dashboard.html', context)


@login_required
def dashboard_redirect_view(request):
    user = request.user

    if user.role in ['worker', 'manager']:
        return redirect('worker_dashboard')
    elif user.role == 'reviewer':
        return redirect('reviewer_dashboard')
    elif user.role == 'admin':
        return redirect('admin_dashboard')

    messages.warning(request, "Your account role is not recognized.")
    return redirect('login')


# @login_required
# @role_required(['worker', 'manager'])
# def worker_dashboard_view(request):
#     return render(request, 'accounts/worker_dashboard.html')


@login_required
@role_required(['reviewer'])
def reviewer_dashboard_view(request):
    return render(request, 'accounts/reviewer_dashboard.html')


@login_required
@role_required(['admin'])
def admin_dashboard_view(request):
    total_users = User.objects.count()
    total_submissions = Submission.objects.count()
    approved_cases = Submission.objects.filter(status='approved').count()

    system_alerts = Submission.objects.filter(
        status__in=['pending_ai', 'pending_review']
    ).count()

    context = {
        'total_users': total_users,
        'total_submissions': total_submissions,
        'approved_cases': approved_cases,
        'system_alerts': system_alerts,
    }

    return render(request, 'accounts/admin_dashboard.html', context)



@login_required
@role_required(['admin'])
def admin_user_list_view(request):
    search_query = request.GET.get('q', '')
    role_filter = request.GET.get('role', '')

    users = User.objects.all().order_by('-date_joined')

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    if role_filter:
        users = users.filter(role=role_filter)

    context = {
        'users': users,
        'search_query': search_query,
        'role_filter': role_filter,
        'role_choices': User.ROLE_CHOICES,
    }
    return render(request, 'accounts/admin_user_list.html', context)


@login_required
@role_required(['admin'])
def admin_user_create_view(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('admin_user_list')
    else:
        form = AdminUserCreationForm()

    return render(request, 'accounts/admin_user_form.html', {
        'form': form,
        'page_title': 'Create User',
        'submit_text': 'Create User',
    })


@login_required
@role_required(['admin'])
def admin_user_update_view(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('admin_user_list')
    else:
        form = AdminUserUpdateForm(instance=user_obj)

    return render(request, 'accounts/admin_user_form.html', {
        'form': form,
        'page_title': f'Edit User: {user_obj.username}',
        'submit_text': 'Update User',
        'user_obj': user_obj,
    })


@login_required
@role_required(['admin'])
def admin_user_delete_view(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    if request.user == user_obj:
        messages.error(request, "You cannot delete your own account.")
        return redirect('admin_user_list')

    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('admin_user_list')

    return redirect('admin_user_list')



@login_required
@role_required(['reviewer'])
def reviewer_dashboard_view(request):
    total_pending_reviews = Submission.objects.filter(status='pending_review').count()
    approved_today = Submission.objects.filter(status='approved').count()
    corrected_cases = Submission.objects.filter(status='reviewed').count()
    rejected_cases = Submission.objects.filter(status='rejected').count()

    context = {
    'total_pending_reviews': total_pending_reviews,
    'approved_today': approved_today,
    'corrected_cases': corrected_cases,
    'rejected_cases': rejected_cases,
}
    return render(request, 'accounts/reviewer_dashboard.html', context)