from django.urls import path

from . import views

app_name = "onboarding"


urlpatterns = [
    path("", views.onboarding_view, name="onboarding"),
    path("genres/", views.genre_view, name="genres"),
    path("movies/", views.movie_view, name="movies"),
    path(
        "movies/random/<int:amount>/",
        views.get_random_movies,
        name="get_movies",
    ),
    path("movies/search", views.search_movie, name="search_movies"),
    path("imports/", views.import_view, name="import"),
    path("upload/", views.upload, name="upload"),
    path(
        "triggers/",
        views.trigger_view,
        name="triggers",
    ),
    path(
        "streaming/",
        views.streaming_view,
        name="streaming",
    ),
]
