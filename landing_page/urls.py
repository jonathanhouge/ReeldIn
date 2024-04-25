from django.urls import path, include
from . import views
from accounts.views import get_random_movies
from django.conf import settings
from django.conf.urls.static import static

app_name = "landing_page"

urlpatterns = [
    path("", views.index, name="index"),
    path("get-csrf-token/", views.get_csrf_token, name="get_csrf_token"),
    path("about/", views.about, name="about"),
    path("profile/", views.profile, name="profile"),
    path("contact/", views.contact, name="contact"),
    path("search/movies", views.search_movies, name="search_movies"),
    path("movie/<int:movie_id>", views.movie, name="movie"),
    path("api/search/movies", views.search_movies_json, name="search_movies_json"),
    path("api/movies/", get_random_movies, name="get_movies"),
]

# TODO this allows for media to be served in development, change in production#
# Link for production: https://docs.djangoproject.com/en/5.0/howto/static-files/deployment/
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
