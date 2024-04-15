import json
import os

from django.conf import settings
from django.db.models import CharField, Q, TextField
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from fuzzywuzzy import fuzz

from recommendations.models import Movie


# Initial landing page view.
def index(request):
    return render(request, "landing_page/index.html")


def about(request):
    return render(request, "landing_page/about.html")


def contact(request):
    return render(request, "landing_page/contact.html")


def about(request):
    return render(request, "landing_page/about.html")


# testing purposes
def movie(request):
    return render(request, "landing_page/movie.html")


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrf_token": csrf_token})


def sort_by_closeness(query, movie):
    return fuzz.partial_ratio(query, movie.name)


def search_movies(request):
    query = request.GET.get("query")

    if query:
        # Construct Q objects for name, director, and release_year fields
        q_name = Q(name__icontains=query)
        q_director = Q(director__icontains=query)
        q_release_year = Q(year__icontains=query)

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
            movies = Movie.objects.filter(name__icontains=search_string).order_by(
                "name"
            )[:5]
        else:
            movies = Movie.objects.none()

        result = {"movies": list(movies.values())}  # Your search result data here

        # Return the result as JSON response
        return JsonResponse(result, safe=False)

    # Return an error response for non-POST requests
    return JsonResponse({"error": "Method not allowed"}, status=405)
