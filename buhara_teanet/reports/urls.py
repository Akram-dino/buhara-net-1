from django.urls import path
from . import views

urlpatterns = [
    path('submission/<int:pk>/', views.submission_report_pdf_view, name='submission_report_pdf'),
    path('analytics/', views.analytics_report_pdf_view, name='analytics_report_pdf'),
    path('my-report/<str:period>/', views.worker_period_report_pdf_view, name='worker_period_report_pdf'),
]