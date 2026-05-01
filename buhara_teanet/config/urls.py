from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


# urlpatterns = [
#     path('admin/', admin.site.urls),

#     # Built-in Django auth
#     path('accounts/', include('django.contrib.auth.urls')),

#     # Custom accounts routes
#     path('', include('accounts.urls')),

#     # Public home page
#     path('home/', TemplateView.as_view(template_name='home.html'), name='home'),

#     # path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
#     path('submissions/', include('submissions.urls')),

#     path('reviews/', include('reviews.urls')),
#     path('analytics/', include('analytics_app.urls')),
#     path('reports/', include('reports.urls')),
# ]







urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL → login
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # ✅ ADD THIS
    path('accounts/', include('django.contrib.auth.urls')),

    # Your apps
    path('accounts/', include('accounts.urls')),
    path('submissions/', include('submissions.urls')),
    path('reviews/', include('reviews.urls')),
    path('analytics/', include('analytics_app.urls')),
    path('reports/', include('reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)