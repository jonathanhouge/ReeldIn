from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.signup, name="register"),
    path("onboarding/", views.onboarding, name="onboarding"),
    path("settings/", views.settings_view, name="settings"),
    path("remove/friend/", views.remove_friend, name="remove_friend"),
    path("send/friend/", views.send_friend_request, name="add_friend"),
    path("accept/friend/", views.accept_friend_request, name="accept_friend"),
    path(
        "delete/friend_request/",
        views.delete_friend_request,
        name="delete_friend_request",
    ),
]
