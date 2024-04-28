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

        movies_to_update = []

        for entry in data:
            if entry["model"] == "recommendation.movie":
                fields = entry["fields"]
                data_tmdb_id = fields.get("tmdb_id")

                try:
                    movie = Movie.objects.get(tmdb_id=data_tmdb_id)
                except ObjectDoesNotExist:
                    print(f"Movie with data_tmdb_id {data_tmdb_id} does not exist.")
                    continue

                movie.imdb_rating = fields.get("imdb_rating") or 0
                movie.imdb_votes = fields.get("imdb_votes") or 0
                movie.imdb_id = fields.get("imdb_id") or "tt0000000"
                movie.ddd_id = fields.get("ddd_id") or 0
                movie.group_lens_id = fields.get("group_lens_id") or 0
                movies_to_update.append(movie)

        Movie.objects.bulk_update(
            movies_to_update,
            ["imdb_rating", "imdb_votes", "imdb_id", "ddd_id", "group_lens_id"],
        )

        print("Movies updated successfully!")
