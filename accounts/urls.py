from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.login_view, name="forgot_password"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.signup, name="register"),
    path("settings/", views.settings_view, name="settings"),
    # Onboarding paths
    path("onboarding/", views.onboarding_view, name="onboarding"),
    path("onboarding/genres/", views.onboarding_genre_view, name="onboarding_genres"),
    path("onboarding/movies/", views.onboarding_movie_view, name="onboarding_movies"),
    path(
        "onboarding/movies/random/<int:amount>/",
        views.get_random_movies,
        name="get_movies",
    ),
    path("onboarding/movies/search", views.search_movie, name="search_movies"),
    path("onboarding/imports/", views.onboarding_import_view, name="onboarding_import"),
    path("onboarding/upload/", views.onboarding_upload, name="onboarding_upload"),
    path(
        "onboarding/triggers/",
        views.onboarding_trigger_view,
        name="onboarding_triggers",
    ),
    path(
        "onboarding/streaming/",
        views.onboarding_streaming_view,
        name="onboarding_streaming",
    ),
    path(
        "onboarding/delete/",
        views.delete_movie,
        name="delete_movie",
    ),
    # Friend management paths
    path("send/friend/", views.send_friend_request, name="add_friend"),
    path("accept/friend/", views.accept_friend_request, name="accept_friend"),
    path("remove/friend/", views.remove_friend, name="remove_friend"),
    path(
        "delete/friend_request/",
        views.delete_friend_request,
        name="delete_friend_request",
    ),
    # Settings paths
    path("change/password/", views.change_password, name="change_password"),
    path("change/username/", views.change_username, name="change_username"),
    path("delete/account/", views.delete_account, name="delete_account"),
    # Miscellaneous
    path("delete_movies", views.delete_movies_view, name="delete_movies"),
    path("clear/lists/", views.clear_lists, name="clear_lists"),
    path(
        "preferences/movies/", views.preferences_movies_view, name="preferences_movies"
    ),
    path(
        "preferences/movies/<int:id>/",
        views.preferences_single_movie_view,
        name="preferences_movies",
    ),
]
