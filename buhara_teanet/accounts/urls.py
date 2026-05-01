from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_redirect_view, name='dashboard'),
    path('dashboard/worker/', views.worker_dashboard_view, name='worker_dashboard'),
    path('dashboard/reviewer/', views.reviewer_dashboard_view, name='reviewer_dashboard'),
    path('dashboard/admin/', views.admin_dashboard_view, name='admin_dashboard'),
    path('manage/users/', views.admin_user_list_view, name='admin_user_list'),
    path('manage/users/create/', views.admin_user_create_view, name='admin_user_create'),
    path('manage/users/<int:pk>/edit/', views.admin_user_update_view, name='admin_user_update'),
    path('manage/users/<int:pk>/delete/', views.admin_user_delete_view, name='admin_user_delete'),
    ]