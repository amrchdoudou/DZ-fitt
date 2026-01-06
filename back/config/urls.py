from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    # Admin Django
    path("admin/", admin.site.urls),

    # App API
    path("api/", include("app.urls")),

    # Allauth URLs at root (this is needed for Google login)
    path("accounts/", include("allauth.urls")),

    # DJ Rest Auth for API authentication
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/auth/social/", include("allauth.socialaccount.urls")),
]

# Media files in DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
