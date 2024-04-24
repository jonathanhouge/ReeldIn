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
    watched_films = models.ManyToManyField(
        Movie, related_name="users_seen", default=list, blank=True
    )
    recommended_films = models.ManyToManyField(
        Movie, related_name="users_recommended", default=list, blank=True
    )
    watchlist_films = models.ManyToManyField(
        Movie, related_name="users_watchlisted", default=list, blank=True
    )
    liked_films = models.ManyToManyField(
        Movie, related_name="users_liked", default=list, blank=True
    )
    disliked_films = models.ManyToManyField(
        Movie, related_name="users_disliked", default=list, blank=True
    )
    # TODO uncomment when ready
    # films_to_rewatch = models.ManyToManyField(
    #     Movie, related_name="users_to_rewatch", default=list, blank=True
    # )
    # films_dont_recommend = models.ManyToManyField(
    #     Movie, related_name="users_dont_recommend", default=list, blank=True
    # )
    # subscriptions = ArrayField(
    #     models.CharField(max_length=13, choices=SERVICES), default=list, blank=True
    # )
    # preferences
    liked_genres = ArrayField(
        models.CharField(max_length=13, choices=GENRES), default=list, blank=True
    )
    disliked_genres = ArrayField(
        models.CharField(max_length=13, choices=GENRES), default=list, blank=True
    )
    liked_cast_and_crew = ArrayField(
        models.CharField(max_length=100), default=list, blank=True
    )
    disliked_cast_and_crew = ArrayField(
        models.CharField(max_length=100), default=list, blank=True
    )
    triggers = ArrayField(
        models.CharField(max_length=100, choices=TRIGGERS), default=list, blank=True
    )


# shout-out to: https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
class FriendRequest(models.Model):
    sender = models.ForeignKey(
        "User", related_name="from_user", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        "User", related_name="to_user", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("sender", "receiver")  # Ensures no duplicate requests
