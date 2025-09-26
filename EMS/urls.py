
"""EMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""

from django.urls import path, re_path, include
from django.contrib import admin
from event import views as event_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("event/", include(("event.urls", "event"), namespace="event")),
    path("user/", include(("user.urls", "user"), namespace="user")),
    path("", include(("event.urls", "event"), namespace="event-root")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler400 = event_views.custom_bad_request
handler403 = event_views.custom_permission_denied
handler404 = event_views.custom_page_not_found
handler500 = event_views.custom_server_error