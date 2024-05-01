"""
This file is meant to update the database with the corrected ddd ID from 
the '7movie_fixture.json' file, although any JSON fixture could be used. 
"""

from django.core.management.base import BaseCommand
from recommendations.models import Movie
from django.core.exceptions import ObjectDoesNotExist
import json


class Command(BaseCommand):
    help = "Updates movies from a JSON fixture"

    def add_arguments(self, parser):
        parser.add_argument(
            "fixture_file", type=str, help="Path to the JSON fixture file"
        )

    def handle(self, *args, **options):
        with open(options["fixture_file"], "r") as file:
            data = json.load(file)

        movies_to_update = set()

        for entry in data:
            if entry["model"] == "recommendation.movie":
                fields = entry["fields"]
                data_tmdb_id = fields.get("tmdb_id")

                try:
                    movie = Movie.objects.get(tmdb_id=data_tmdb_id)
                except ObjectDoesNotExist:
                    print(f"Movie with data_tmdb_id {data_tmdb_id} does not exist.")
                    continue

                movie.ddd_id = fields.get("ddd_id") or 0
                movies_to_update.add(movie)

        Movie.objects.bulk_update(
            movies_to_update,
            ["ddd_id"],
        )

        print("Movies updated successfully!")
