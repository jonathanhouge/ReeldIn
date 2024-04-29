import json
import os
import requests

from django.conf import settings
from django.db.models import CharField, Q, TextField
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, redirect, render
from fuzzywuzzy import fuzz
from django.core.serializers import serialize

from recommendations.models import Movie, RecentRecommendations
from recommendations.helpers import make_readable_recommendation
from recommendations.choices import LANGUAGES
from accounts.models import FriendRequest


def index(request):
    try:
        all_recommendations = RecentRecommendations.objects.get(id=1)
    except:
        all_recommendations = RecentRecommendations()
        all_recommendations.save()

    readable_recommendations = make_readable_recommendation(
        all_recommendations.recent.all()
    )

    return render(
        request,
        "landing_page/index.html",
        {"recommendations": readable_recommendations},
    )


def about(request):
    return render(request, "landing_page/about.html")


def contact(request):
    return render(request, "landing_page/contact.html")


def profile(request):
    if not request.user.is_authenticated:
        return render(request, "accounts/login.html")

    # Load context with user data
    recommended_movies = list(request.user.recommended_films.values("pk", "poster"))
    watched_movies = list(request.user.watched_films.values("pk", "poster"))
    liked_movies = list(request.user.liked_films.values("pk", "poster"))
    disliked_movies = list(request.user.disliked_films.values("pk", "poster"))
    watchlist_movies = list(request.user.watchlist_films.values("pk", "poster"))
    friends = request.user.friends.all()
    sent_requests = FriendRequest.objects.filter(sender=request.user)
    received_requests = FriendRequest.objects.filter(receiver=request.user)

    context = {
        "recommended_movies": recommended_movies,
        "watched_movies": watched_movies,
        "liked_movies": liked_movies,
        "disliked_movies": disliked_movies,
        "watchlist_movies": watchlist_movies,
        "friends": friends,
        "sent_requests": sent_requests,
        "received_requests": received_requests,
    }

    return render(request, "accounts/profile.html", context)


# testing purposes
def movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie_json = serialize("json", [movie])
    movie_json = json.loads(movie_json)[0]["fields"]

    language_dict = dict(LANGUAGES)  # from rec/helpers
    movie_json["language"] = language_dict.get(movie.language)

    return render(
        request, "landing_page/movie.html", {"movie": movie, "movie_json": movie_json}
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
        q_name = Q(name__istartswith=query)
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
            "landing_page/search.html",
            context={
                "movies": sorted_movies,
                "WATCHMODE_API_KEY": os.environ.get("WATCHMODE_API_KEY"),
            },
        )

    return redirect("")


def search_movies_json(request):
    if request.method == "POST":
        # Decode the request body
        body_unicode = request.body.decode("utf-8")

        # Parse the JSON data
        body_data = json.loads(body_unicode)

        # Access specific fields from the JSON data
        search_string = body_data.get("search")

        if search_string:
            movies = Movie.objects.filter(name__istartswith=search_string)
            sorted_movies = sorted(
                movies,
                key=lambda movie: sort_by_closeness(search_string, movie),
                reverse=True,
            )[:5]
        else:
            sorted_movies = Movie.objects.none()

        result = {
            "movies": [
                {
                    "id": movie.id,
                    "name": movie.name,
                    "genres": movie.genres,
                    "starring": movie.starring,
                    "poster": movie.poster,
                    "year": movie.year,
                }
                for movie in sorted_movies
            ]
        }

        # Return the result as JSON response
        return JsonResponse(result, safe=False)

    # Return an error response for non-POST requests
    return JsonResponse({"error": "Method not allowed"}, status=405)


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
