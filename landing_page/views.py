from django.shortcuts import render, redirect
from django.http import JsonResponse
from recommendations.models import Movie
from django.db.models import Q, CharField, TextField


# Initial landing page view.
def index(request):
    return render(request, "landing_page/index.html")


def about(request):
    return render(request, "landing_page/about.html")


def contact(request):
    return render(request, "landing_page/contact.html")


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
        # movies = Movie.objects.filter(*q_objects).distinct()
        # json_movies = [{"movie": movie} for movie in movies]
        json_movies = [
            {"name": "spiderman", "year": 2023},
            {"name": "batman", "year": 1999},
        ]

        return render(request, "landing_page/movie.html", {"movies": json_movies})

    return redirect("")


def search_movies_json(request):
    return {"response": "OK"}
