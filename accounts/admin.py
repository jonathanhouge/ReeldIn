from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from recommendations.models import Movie


class CustomUserAdmin(BaseUserAdmin):
    model = User
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "letterboxd_username",
                    "imdb_user_id",
                    "seen_films",
                    "recommended_films",
                    "would_rewatch",
                    "movies_liked",
                    "movies_disliked",
                    "movies_blocked",
                    "movie_watchlist",
                    "liked_genres",
                    "disliked_genres",
                    "blocked_genres",
                    "liked_people",
                    "disliked_people",
                    "blocked_people",
                )
            },
        ),
        ("Relationships", {"fields": ("friends", "blocked_users")}),
    )
    filter_horizontal = (
        "seen_films",
        "recommended_films",
        "would_rewatch",
        "movies_liked",
        "movies_disliked",
        "movies_blocked",
        "movie_watchlist",
        "friends",
    )


admin.site.register(User, CustomUserAdmin)
