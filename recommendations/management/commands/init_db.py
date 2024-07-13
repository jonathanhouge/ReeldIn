"""
This file holds the functionality for initializing the database with the JSON fixture file,
located in recommendations/fixtures/movies_fixture.json.

Created in order to speed up the process of loading data into the database
via bulk_create as the file's size causes 'loaddata' to be inefficient.
"""

import json
from django.core.management.base import BaseCommand
from django.db import transaction
from recommendations.models import Movie


class Command(BaseCommand):
    help = "Loads data from a JSON fixture file into the database efficiently"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Path to the JSON fixture file")

    def handle(self, *args, **kwargs):
        file_path = kwargs["json_file"]
        try:
            with open(file_path, "r") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("JSON data should be a list of entries.")

            movies_to_create = []
            batch_size = 1000
            for entry in data:
                fields = entry["fields"]
                movie = Movie(
                    name=fields.get("name"),
                    year=fields.get("year"),
                    genres=fields.get("genres"),
                    runtime=fields.get("runtime"),
                    language=fields.get("language"),
                    budget=fields.get("budget"),
                    revenue=fields.get("revenue"),
                    poster=fields.get("poster"),
                    overview=fields.get("overview"),
                    tagline=fields.get("tagline"),
                    starring=fields.get("starring"),
                    director=fields.get("director"),
                    writer=fields.get("writer"),
                    cinematographer=fields.get("cinematographer"),
                    composer=fields.get("composer"),
                    watch_providers=fields.get("watch_providers"),
                    keywords=fields.get("keywords"),
                    tmdb_id=fields.get("tmdb_id"),
                    imdb_rating=fields.get("imdb_rating") or 0,
                    imdb_votes=fields.get("imdb_votes") or 0,
                    imdb_id=fields.get("imdb_id") or "tt0000000",
                    ddd_id=fields.get("ddd_id") or 0,
                    group_lens_id=fields.get("group_lens_id") or 0,
                )
                movies_to_create.append(movie)

                if len(movies_to_create) >= batch_size:
                    with transaction.atomic():
                        Movie.objects.bulk_create(movies_to_create)
                    movies_to_create = []

            # create any remaining instances
            with transaction.atomic():
                Movie.objects.bulk_create(movies_to_create)

            print("Data loaded successfully.")

        except Exception as e:
            print(f"An error occurred:\n{e}")
