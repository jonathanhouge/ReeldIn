from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.login_view, name="forgot_password"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.signup, name="register"),
    path("settings/", views.settings_view, name="settings"),
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
    path(
        "preferences/movies/", views.preferences_movies_view, name="preferences_movies"
    ),
    path(
        "preferences/movies/<int:id>/",
        views.preferences_single_movie_view,
        name="preferences_movies",
    ),
]
