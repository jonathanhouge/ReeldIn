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
]
