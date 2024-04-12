from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from recommendations.models import Movie
from django.db.models import Q, CharField, TextField
from django.middleware.csrf import get_token
import json
from django.core.serializers import serialize
from functools import reduce
from operator import or_


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


def search_movies(request):
    query = request.GET.get("query")

    if query:
        # Get all field names of the Movie model
        movie_fields = [
            field.name
            for field in Movie._meta.get_fields()
            if isinstance(field, (CharField, TextField))
        ]

        # Construct a list of Q objects for each field
        q_objects = [Q(**{f"{field}__icontains": query}) for field in movie_fields]

        # Combine all Q objects using OR operator
        query_filter = reduce(or_, q_objects)
        movies = Movie.objects.filter(query_filter).distinct().order_by("name")
        json_movies = list(movies.values())

        return render(request, "landing_page/search.html", {"movies": json_movies})

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
