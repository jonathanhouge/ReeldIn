from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class CustomUserAdmin(BaseUserAdmin):
    model = User
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "letterboxd_username",
                    "imdb_user_id",
                    "watched_films",
                    "recommended_films",
                    "watchlist_films",
                    "liked_films",
                    "disliked_films",
                    "liked_genres",
                    "disliked_genres",
                    "liked_cast_and_crew",
                    "disliked_cast_and_crew",
                    "triggers",
                )
            },
        ),
        ("Relationships", {"fields": ("friends",)}),
    )
    filter_horizontal = (
        "friends",
        "watched_films",
        "recommended_films",
        "watchlist_films",
        "liked_films",
        "disliked_films",
    )


admin.site.register(User, CustomUserAdmin)
