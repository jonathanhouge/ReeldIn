import csv
import json

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from fuzzywuzzy import fuzz

from recommendations.choices import STREAMING, TRIGGERS
from recommendations.models import Movie

from .forms import CustomBooleanForm, GenreForm
from .helpers import (
    add_movies_to_user_list,
    get_genre_form_data,
    get_user_genre_preferences,
)

MOVIES_POST_TO_MODEL = {  # maps the POST request names to the model names
    "movies_liked": "liked_films",
    "movies_disliked": "disliked_films",
    "movies_watched": "watched_films",
    "watchlist": "watchlist_films",
    "movies_rewatch": "rewatchable_films",
    "movies_blocked": "excluded_films",
}
MIN_LIKED_RATING_LETTERBOXD = 3.0
MIN_LIKED_RATING_IMDB = 6.5
def onboarding_view(request):
    """
    The intro page is only visible to users who have just signed up.
    """
    if request.session.get("onboarding"):
        return render(
            request,
            "onboarding/onboarding.html",
        )
    return redirect("landing_page:index")


def genre_view(request):
    """
    This function handles the POST/GET requests for the onboarding genre form.
    """
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            liked_genres, disliked_genres, blocked_genres = get_genre_form_data(form)
            with transaction.atomic():
                request.user.liked_genres = liked_genres
                request.user.disliked_genres = disliked_genres
                request.user.excluded_genres = blocked_genres
                request.user.save()
            return redirect("/onboarding/imports/")
    else:
        initial_data = get_user_genre_preferences(request.user)
        form = GenreForm(initial_preferences=initial_data)
    return render(request, "onboarding/genres.html", {"form": form})


def movie_view(request):
    """
    This function handles the POST/GET requests for the onboarding movie form.
    POST saves the user's preferences while GET renders the page.
    """
    if request.method != "POST":
        return render(
            request,
            "onboarding/movies.html",
        )

    data = json.loads(request.body)

    with transaction.atomic():
        for post_name, model_name in MOVIES_POST_TO_MODEL.items():
            movie_list = data.get(post_name, [])
            add_movies_to_user_list(request.user, movie_list, model_name)

        return HttpResponse(status=200)


def add_movies_to_user_list(user, movie_list, model_name):
    """
    This helper function adds the movies in movie_list
    to the list specified by model_name for the user.
    """
    users_list = getattr(user, model_name)
    current_movies = set(users_list.values_list("id", flat=True))

    new_movie_set = set(movie_list)

    # TODO ideally do this before the POST (on the client side)
    movies_to_add = new_movie_set - current_movies
    movies_to_remove = current_movies - new_movie_set

    if movies_to_remove:
        users_list.remove(*Movie.objects.filter(id__in=movies_to_remove))
    if movies_to_add:
        users_list.add(*Movie.objects.filter(id__in=movies_to_add))


def import_view(request):
    return render(request, "onboarding/imports.html")


# Sends file to either IMDb or Letterboxd data handling functions
def upload(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    if "document" not in request.FILES:
        return HttpResponse("No file uploaded", status=400)

    try:
        if request.FILES["document"].name.endswith(".csv") == False:
            request.user.profile_picture = request.FILES["document"]
            return HttpResponse("Profile picture uploaded", status=200)
    except AttributeError:
        return HttpResponse("Invalid file format", status=400)

    uploaded_file = request.FILES["document"]
    file_object = uploaded_file.file
    decoded_file = file_object.read().decode("utf-8").splitlines()

    reader = csv.reader(decoded_file)
    columns = next(reader)
    try:
        if columns[0] == "Const" and columns[1] == "Your Rating":
            add_IMDb_Data(reader, request.user)
        elif columns[1] == "Name" and columns[2] == "Year" and columns[4] == "Rating":
            add_Letterboxd_Data(reader, request.user)
        else:
            return HttpResponse(
                "Invalid file format. Please make sure you're uploading the correct file.",
                status=400,
            )
    except IndexError:
        return HttpResponse("Invalid file format", status=400)

    return HttpResponse("File uploaded", status=200)


# Adds IMDb data to the user's liked and disliked lists
def add_IMDb_Data(reader, user):
    blocked_list = getattr(user, "excluded_films")
    liked_list = getattr(user, "liked_films")
    disliked_list = getattr(user, "disliked_films")
    watched_list = getattr(user, "watched_films")

    blocked_movies = set(blocked_list.values_list("imdb_id", flat=True))
    liked_movies = set(liked_list.values_list("imdb_id", flat=True))
    disliked_movies = set(disliked_list.values_list("imdb_id", flat=True))
    watched_movies = set(watched_list.values_list("imdb_id", flat=True))

    all_movies = set(blocked_movies | liked_movies | disliked_movies | watched_movies)

    new_liked = set()
    new_disliked = set()
    new_watched = set()

    for row in reader:
        tt_id = row[0]
        user_rating = row[1]

        if tt_id == "" or user_rating == "":
            continue

        if tt_id in all_movies:
            continue
        else:
            new_watched.add(tt_id)
            if int(user_rating) >= MIN_LIKED_RATING_IMDB:
                new_liked.add(tt_id)
            elif int(user_rating) < MIN_LIKED_RATING_IMDB:
                new_disliked.add(tt_id)

    liked_list.add(*Movie.objects.filter(imdb_id__in=new_liked))
    disliked_list.add(*Movie.objects.filter(imdb_id__in=new_disliked))
    watched_list.add(*Movie.objects.filter(imdb_id__in=new_watched))

    return HttpResponse("Done", status=200)


# Adds Letterboxd data to the user's liked and disliked lists
def add_Letterboxd_Data(reader, user):
    blocked_list = getattr(user, "excluded_films")
    liked_list = getattr(user, "liked_films")
    disliked_list = getattr(user, "disliked_films")
    watched_list = getattr(user, "watched_films")

    blocked_movies = set(blocked_list.values_list("imdb_id", flat=True))
    watched_movies = set(watched_list.values_list("imdb_id", flat=True))
    liked_movies = set(liked_list.values_list("imdb_id", flat=True))
    disliked_movies = set(disliked_list.values_list("imdb_id", flat=True))

    all_movies = set(blocked_movies | liked_movies | disliked_movies | watched_movies)

    liked_data = set()
    disliked_data = set()
    new_watched = set()

    for row in reader:
        movie_data = (row[1], row[2], row[4])
        movie_name, movie_year, rating = movie_data

        if movie_name == "" or movie_year == "" or rating == "":
            continue

        movie = Movie.objects.filter(name=movie_name, year=movie_year).first()

        if movie is None:
            continue
        if movie.imdb_id in all_movies and movie.imdb_id not in new_watched:
            continue
        new_watched.add(movie.imdb_id)

        if float(rating) >= MIN_LIKED_RATING_LETTERBOXD:
            liked_data.add(movie.imdb_id)
        else:
            disliked_data.add(movie.imdb_id)

    liked_list.add(*Movie.objects.filter(imdb_id__in=liked_data))
    disliked_list.add(*Movie.objects.filter(imdb_id__in=disliked_data))
    watched_list.add(*Movie.objects.filter(imdb_id__in=new_watched))

    return HttpResponse("Done", status=200)


def trigger_view(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    user = request.user

    if request.method == "POST":
        form = CustomBooleanForm(request.POST, items=TRIGGERS)
        if form.is_valid():

            user.triggers = [
                trigger_value
                for trigger_value, checked in form.cleaned_data.items()
                if checked
            ]

            user.save()

            return redirect("/onboarding/streaming")
    else:
        initial_data = {trigger: True for trigger in user.triggers}
        form = CustomBooleanForm(items=TRIGGERS, initial_preferences=initial_data)
    return render(request, "onboarding/triggers.html", {"form": form})


def streaming_view(request):

    if not request.user.is_authenticated:
        return redirect("accounts:login")

    user = request.user
    if request.method == "POST":
        form = CustomBooleanForm(request.POST, items=STREAMING)
        if form.is_valid():
            user.subscriptions = [
                subscription_value
                for subscription_value, checked in form.cleaned_data.items()
                if checked
            ]
            user.save()
            if request.session.get("onboarding"):
                request.session["onboarding"] = False
                return redirect("recommendations:index")
            return redirect("accounts:settings")
    else:
        initial_data = {service: True for service in user.subscriptions}
        form = CustomBooleanForm(items=STREAMING, initial_preferences=initial_data)
    return render(request, "onboarding/streaming.html", {"form": form})


def get_random_movies(request, amount=25):
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


# TODO this is also in the langing_page/accounts apps
# TODO should go in the movies app
def sort_by_closeness(query, movie):
    return fuzz.ratio(query, movie.name)


# TODO separate method/path as this method handles both movie deletion search/onboarding search
# TODO once deletion search is isolated, data not used during onboarding can be removed
# TODO this should go in the movies app, currently in both the accounts and landing_page apps
def search_movie(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    # Decode the request body
    body_unicode = request.body.decode("utf-8")

    # Parse the JSON data
    body_data = json.loads(body_unicode)

    # Access specific fields from the JSON data
    search_string = body_data.get("search")

    if search_string:
        movies = Movie.objects.filter(name__icontains=search_string)
        sorted_movies = sorted(
            movies,
            key=lambda movie: sort_by_closeness(search_string, movie),
            reverse=True,
        )
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
