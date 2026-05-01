from django.urls import path
from . import views

urlpatterns = [
    path('', views.submission_list_view, name='submission_list'),
    path('upload/', views.submission_create_view, name='submission_create'),
    path('<int:pk>/', views.submission_detail_view, name='submission_detail'),
    path('<int:pk>/delete/', views.submission_delete_view, name='submission_delete'),
    path('<int:pk>/edit/', views.submission_update_view, name='submission_update'),
]