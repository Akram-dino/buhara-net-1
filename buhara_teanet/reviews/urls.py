from django.urls import path
from . import views

urlpatterns = [
    path('', views.reviewer_submission_list_view, name='reviewer_submission_list'),
    path('<int:pk>/', views.reviewer_submission_detail_view, name='reviewer_submission_detail'),
]