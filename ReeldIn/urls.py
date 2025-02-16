"""
ReeldIn URL Configuration

For more information please see:
https://docs.djangoproject.com/en/4.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("landing_page.urls", namespace="landing_page")),
    path("base/", include("base.urls", namespace="base")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path(
        "recommendations/", include("recommendations.urls", namespace="recommendations")
    ),
    path("__reload__/", include("django_browser_reload.urls")),
    path("error/", include("base.urls", namespace="error")),
    path("dev_tools/", include("dev_tools.urls", namespace="dev_tools")),
]
