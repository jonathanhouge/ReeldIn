from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError

from .choices import *


class Movie(models.Model):
    name = models.CharField(max_length=105)
    genres = ArrayField(models.CharField(max_length=13, choices=GENRES))
    year = models.PositiveIntegerField()
    runtime = models.PositiveIntegerField()
    language = models.CharField(max_length=2, choices=LANGUAGES)
    budget = models.BigIntegerField(default=0)
    revenue = models.BigIntegerField(default=0)

    poster = models.TextField()
    overview = models.TextField()
    tagline = models.TextField()

    # people
    starring = ArrayField(models.CharField(max_length=60))
    director = ArrayField(models.CharField(max_length=60))
    writer = ArrayField(models.CharField(max_length=60))
    cinematographer = ArrayField(models.CharField(max_length=60))
    composer = ArrayField(models.CharField(max_length=60))

    watch_providers = ArrayField(models.CharField(max_length=60, choices=STREAMING))
    keywords = ArrayField(models.CharField(max_length=60))
    tmdb_id = models.PositiveIntegerField()
    imdb_rating = models.DecimalField(max_digits=10, decimal_places=2)
    imdb_votes = models.PositiveIntegerField()


class Recommendation(models.Model):
    user_id = models.OneToOneField(
        "accounts.User", unique=True, on_delete=models.CASCADE, default=0
    )
    step = models.PositiveIntegerField(default=1)
    possible_films = models.ManyToManyField(
        "Movie", related_name="possible_recommendations", blank=True
    )
    possible_film_count = models.PositiveIntegerField(default=27122)
    recommended_films = models.ManyToManyField(
        "Movie", related_name="recommendations", blank=True
    )

    # answers
    genres = ArrayField(
        models.CharField(max_length=13, choices=GENRES), null=True, blank=True
    )
    year_span = models.CharField(
        max_length=9, choices=YEAR_SPANS, null=True, blank=True
    )
    runtime_span = models.CharField(
        max_length=7, choices=RUNTIME_SPANS, null=True, blank=True
    )
    languages = ArrayField(
        models.CharField(max_length=2, choices=LANGUAGES), null=True, blank=True
    )
    triggers = ArrayField(
        models.CharField(max_length=100, choices=TRIGGERS), null=True, blank=True
    )
    watch_providers = ArrayField(
        models.CharField(max_length=60, choices=STREAMING), null=True, blank=True
    )

    preferred_cast = ArrayField(models.CharField(max_length=60), null=True, blank=True)
    preferred_crew = ArrayField(models.CharField(max_length=60), null=True, blank=True)
    excluded_cast = ArrayField(models.CharField(max_length=60), null=True, blank=True)
    excluded_crew = ArrayField(models.CharField(max_length=60), null=True, blank=True)

    popular = models.BooleanField(default=False)
    well_reviewed = models.BooleanField(default=True)
    external_account_influence = models.BooleanField(default=False)

    # TODO jokey questions


# only one of these - populates the front page
class RecentRecommendations(models.Model):
    recent = models.ManyToManyField(
        "Movie", related_name="recently_recommended", blank=True
    )

    def save(self, *args, **kwargs):
        if not self.pk and RecentRecommendations.objects.exists():
            raise ValidationError("There can only be one!")
        return super(RecentRecommendations, self).save(*args, **kwargs)
