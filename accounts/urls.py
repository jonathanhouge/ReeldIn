from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.signup, name="register"),
    path("onboarding/", views.onboarding, name="onboarding"),
    path("onboarding/genres/", views.onboarding_genre_view, name="onboarding_genres"),
    path("onboarding/movies/", views.onboarding_movie_view, name="onboarding_movies"),
    path("settings/", views.settings_view, name="settings"),
    path(
        "preferences/movies/", views.preferences_movies_view, name="preferences_movies"
    ),
    path(
        "onboarding/triggers/",
        views.onboarding_trigger_view,
        name="onboarding_triggers",
    ),
    path("remove/friend/", views.remove_friend, name="remove_friend"),
    path("send/friend/", views.send_friend_request, name="add_friend"),
    path("accept/friend/", views.accept_friend_request, name="accept_friend"),
    path(
        "delete/friend_request/",
        views.delete_friend_request,
        name="delete_friend_request",
    ),
]
