import json
import os
import re

import requests
from django.conf import settings
from django.core.serializers import serialize
from django.db.models import CharField, Q, TextField
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, redirect, render
from fuzzywuzzy import fuzz

from accounts.models import FriendRequest
from recommendations.choices import LANGUAGES
from recommendations.helpers import make_readable_recommendation
from recommendations.models import Movie, RecentRecommendations


# testing purposes
def movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie_json = serialize("json", [movie])
    movie_json = json.loads(movie_json)[0]["fields"]
    movie_json["id"] = movie_id

    language_dict = dict(LANGUAGES)  # from rec/helpers
    movie_json["language"] = language_dict.get(movie.language)

    # remove duplicate writers (string to list, remove duplicates, json readable)
    writers_list = re.sub(r"[\[\]\"]", "", movie_json["writer"]).split(", ")
    movie_json["writer"] = json.dumps(list(set(writers_list)))

    return render(
        request, "movies/movie.html", {"movie": movie, "movie_json": movie_json}
    )


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrf_token": csrf_token})


def sort_by_closeness(query, movie):
    return fuzz.ratio(query, movie.name)


def search_movies(request):
    query = request.GET.get("query")

    if query:
        # Construct Q objects for name, director, and release_year fields
        q_name = Q(name__icontains=query)
        q_director = Q(director__istartswith=query)
        q_release_year = Q(year__istartswith=query)

        # Combine Q objects using OR operator
        query_filter = q_name | q_director | q_release_year

        # Query movies matching any of the search criteria
        movies = Movie.objects.filter(query_filter).distinct()
        sorted_movies = sorted(
            movies, key=lambda movie: sort_by_closeness(query, movie), reverse=True
        )

        return render(
            request,
            "movies/search.html",
            context={
                "movies": sorted_movies,
            },
        )

    return redirect("")


def search_movies_json(request):
    if request.method != "POST":
        # Return an error response for non-POST requests
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # Decode the request body
    body_unicode = request.body.decode("utf-8")

    # Parse the JSON data
    body_data = json.loads(body_unicode)

    # Access specific fields from the JSON data
    search_string = body_data.get("search")
    limit = body_data.get("limit")

    if search_string:
        movies = Movie.objects.filter(name__icontains=search_string)
        sorted_movies = sorted(
            movies,
            key=lambda movie: sort_by_closeness(search_string, movie),
            reverse=True,
        )
        if limit:
            sorted_movies = sorted_movies[:limit]
    else:
        sorted_movies = Movie.objects.none()

    result = {
        "movies": [
            {
                "id": movie.pk,
                "name": movie.name,
                "poster": movie.poster,
                "year": movie.year,
                "genres": movie.genres,
                "starring": movie.starring,
                "overview": movie.overview,
                "imdb_rating": movie.imdb_rating,
                "imdb_votes": movie.imdb_votes,
                "runtime": movie.runtime,
            }
            for movie in sorted_movies
        ]
    }

    # Return the result as JSON response
    return JsonResponse(result, safe=False)


def random_movies_json(request, amount=25):
    """
    This function returns a JSON response containing a list of random movies
    specified by the amount parameter in the GET request. It is used in
    the movie onboarding process.
    """

    movies = Movie.objects.order_by("?")[:amount]

    data = [
        {
            "id": movie.pk,
            "name": movie.name,
            "poster": movie.poster,
            "year": movie.year,
            "genres": movie.genres,
            "starring": movie.starring,
            "overview": movie.overview,
            "imdb_rating": movie.imdb_rating,
            "imdb_votes": movie.imdb_votes,
            "runtime": movie.runtime,
        }
        for movie in movies
    ]
    return JsonResponse({"movies": data})


# TODO in-progress
def get_mpaa(requests, movie_id):
    """
    This function takes in a movie and returns the MPAA rating of the movie.
    """
    API_KEY = os.environ.get("TMBD_API_KEY")
    url = (
        "https://api.themoviedb.org/3/movie/"
        + str(movie_id)
        + "/release_dates?api_key="
        + API_KEY
    )
    response = requests.get(url)
    data = response.json()
    for result in data["results"]:
        if result["iso_3166_1"] == "US":
            return result["certification"]
    return None


def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)


def update_preference(request, type, movie_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=403)
    elif request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user = request.user

    if type == "liked":
        handle_preference_change(user.liked_films, movie_id)
    elif type == "disliked":
        handle_preference_change(user.disliked_films, movie_id)
    elif type == "rewatch":
        handle_preference_change(user.rewatchable_films, movie_id)
    elif type == "exclude":
        handle_preference_change(user.excluded_films, movie_id)
    elif type == "watchlist":
        handle_preference_change(user.watchlist_films, movie_id)
    elif type == "watched":
        handle_preference_change(user.watched_films, movie_id)
    else:
        return JsonResponse({"error": "Invalid preference type"}, status=400)
    return HttpResponse(status=200)


def handle_preference_change(user_list, id):
    movie = get_object_or_404(Movie, pk=id)

    if movie in user_list.all():
        user_list.remove(movie)
    else:
        user_list.add(movie)

    return
