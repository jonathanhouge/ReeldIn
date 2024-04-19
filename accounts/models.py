from django.db import models
from django.contrib.auth.models import AbstractUser
from recommendations.models import Movie
from recommendations.choices import GENRES, TRIGGERS
from django.contrib.postgres.fields import ArrayField


class User(AbstractUser):
    username = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=100)  # to account for salting & hashing
    email = models.EmailField(max_length=254)
    friends = models.ManyToManyField("User", blank=True)

    # external accounts, used for connections
    letterboxd_username = models.CharField(
        max_length=15, unique=True, null=True, blank=True
    )
    imdb_user_id = models.CharField(max_length=32, unique=True, null=True, blank=True)

    # 'Movie' connections
    seen_films = models.ManyToManyField(Movie, related_name="users_seen", blank=True)
    recommended_films = models.ManyToManyField(
        Movie, related_name="users_recommended", blank=True
    )
    watchlist_films = models.ManyToManyField(
        Movie, related_name="users_watchlisted", blank=True
    )
    liked_films = models.ManyToManyField(Movie, related_name="users_liked", blank=True)
    disliked_films = models.ManyToManyField(
        Movie, related_name="users_disliked", blank=True
    )

    # preferences
    preferred_genres = ArrayField(
        models.CharField(max_length=13, choices=GENRES), null=True, blank=True
    )
    preferred_triggers = ArrayField(
        models.CharField(max_length=100, choices=TRIGGERS), null=True, blank=True
    )
    preferred_cast_and_crew = ArrayField(
        models.CharField(max_length=100), null=True, blank=True
    )


# shout-out to: https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
class FriendRequest(models.Model):
    sender = models.ForeignKey(
        "User", related_name="from_user", on_delete=models.CASCADE
    )
    receipent = models.ForeignKey(
        "User", related_name="to_user", on_delete=models.CASCADE
    )
