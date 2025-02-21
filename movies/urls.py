from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

app_name = "movies"

urlpatterns = [
    path("search/movies", views.search_movies, name="search_movies"),
    path("movie/<int:movie_id>", views.movie, name="movie"),
    path("api/search/movies/", views.search_movies_json, name="search_movies_json"),
    path("health-check/", views.health_check, name="health_check"),
    path(
        "movie/update/<str:type>/<int:movie_id>/",
        views.update_preference,
        name="update_preference",
    ),
    path("get-csrf-token/", views.get_csrf_token, name="get_csrf_token"),
]
