from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

app_name = "landing_page"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("profile/", views.profile, name="profile"),
    path("contact/", views.contact, name="contact"),
    path("error/", views.error, name="error"),
    path("conditions/", views.conditions, name="conditions"),
]

# TODO this allows for media to be served in development, change in production#
# Link for production: https://docs.djangoproject.com/en/5.0/howto/static-files/deployment/
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
