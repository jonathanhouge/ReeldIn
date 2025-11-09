from django.urls import path

from . import views

app_name = "dev_tools"

urlpatterns = [
    path(
        "delete/",
        views.delete_movie,
        name="delete_movie",
    ),
    path("delete_movies", views.delete_movies_view, name="delete_movies"),
]
