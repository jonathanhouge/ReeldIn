import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.http import JsonResponse
from recommendations.models import (
    Movie,
)  # Adjust the import according to your app structure
import random
from .forms import *
from .models import User
from django.db import transaction

MOVIES_POST_TO_MODEL = {
    "movies_liked": "liked_films",
    "movies_disliked": "disliked_films",
    "movies_watched": "watched_films",
    "watchlist": "watchlist_films",
    # TODO uncomment when ready
    # 'movies_rewatch': 'films_to_rewatch',
    # 'movies_blocked': 'films_dont_recommend'
}


def login_view(request):
    """
    This function handles the POST login request and the GET login request.
    POST attempts to login with the provided credentials while GET simply renders the login page.
    """
    # prevents access by logged in users
    if request.user.is_authenticated:
        return redirect("landing_page:index")

    if request.method == "POST":
        provided_username = request.POST["username"]
        provided_password = request.POST["password"]
        user = authenticate(
            request, username=provided_username, password=provided_password
        )

        if user is not None:
            login(request, user)
            return redirect("landing_page:index")
        else:
            return render(
                request,
                "accounts/login.html",
                {"signin_error": "Invalid username and/or password."},
            )
    elif request.method == "GET":
        return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("landing_page:index")


def signup(request):
    """
    This function handles the POST signup request and the GET signup request.
    POST attempts to create a new user with the provided credentials while
    GET simply renders the login page.
    """
    # prevents access by logged in users
    if request.user.is_authenticated:
        return redirect("landing_page:index")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # request.session["onboarding"] = True TODO link to onboarding later
            # return render(request, "accounts/onboarding.html")
            return redirect("landing_page:index")
        else:
            # taken username?
            provided_username = request.POST["username"]
            if User.objects.filter(username=provided_username).exists():
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "signup_error": "Username has already been taken."},
                )

            # taken email?
            providedEmail = request.POST["email"]
            if User.objects.filter(email=providedEmail).exists():
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "signup_error": "Email address is already in use."},
                )

            # passwords don't match?
            password1 = request.POST["password1"]
            confirm = request.POST["password2"]
            if password1 != confirm:
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "signup_error": "Passwords do not match."},
                )

            # TODO make sure email is valid and password is long enough, has at least six characters, and isn't entirely numeric
            # if all else fails, return whatever the form says
            return render(
                request,
                "accounts/login.html",
                {"form": form, "signup_error": form.errors},
            )
    elif request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "accounts/login.html", {"form": form})


def onboarding(request):
    # if(request.session.get("onboarding")):
    return render(
        request,
        "accounts/onboarding.html",
        {
            "back_action": "redirectToLandingPage()",
            "next_action": "proceedToOnboardingGenreForm()",
            "back_text": "Exit",
            "next_text": "Continue",
        },
    )


def onboarding_genre_view(request):
    """
    This function handles the POST/GET requests for the onboarding genre form.
    """
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            liked_genres = []
            disliked_genres = []
            blocked_genres = []
            for genre, preference in form.cleaned_data.items():
                if preference == "like":
                    liked_genres.append(genre)
                elif preference == "dislike":
                    disliked_genres.append(genre)
                # TODO uncomment ? later elif preference == "block":
                #     blocked_genres.append(genre)
            with transaction.atomic():
                request.user.liked_genres = liked_genres
                request.user.disliked_genres = disliked_genres
                # TODO uncomment ? request.user.blocked_genres = blocked_genres
                request.user.save()
            return redirect("/accounts/onboarding/movies")
    else:
        # Fetch the user's preferences
        liked_genres = request.user.liked_genres
        disliked_genres = request.user.disliked_genres
        # TODO add ? blocked_genres = request.user.blocked_genres

        # Prepare initial data dictionary for the form
        initial_data = {}
        for genre in GENRES:
            genre_value = genre[0]
            if genre_value in liked_genres:
                initial_data[genre_value] = "like"
            elif genre_value in disliked_genres:
                initial_data[genre_value] = "dislike"
            # TODO uncomment ? elif genre_value in blocked_genres:
            #     initial_data[genre_value] = "block"
        form = GenreForm(initial_preferences=initial_data)
    return render(
        request,
        "accounts/onboarding_genres.html",
        {
            "form": form,
            # "back_action": "/landing_page/index",
            "next_action": "submitOnboardingGenreForm()",
            "next_text": "Continue",
        },
    )


def onboarding_movie_view(request):
    """
    This function handles the POST/GET requests for the onboarding movie form.
    POST saves the user's preferences while GET renders the page.
    """
    if request.method == "POST":
        data = json.loads(request.body)

        with transaction.atomic():
            for post_name, model_name in MOVIES_POST_TO_MODEL.items():
                movie_list = data.get(post_name, [])
                add_movies_to_user_list(request.user, movie_list, model_name)

        return HttpResponse(status=200)
    return render(
        request,
        "accounts/onboarding_movies.html",
        {
            "back_action": "redirectToOnboardingGenreForm()",
            "next_action": "submitOnboardingMovieForm()",
            "back_text": "Back",
            "next_text": "Continue",
        },
    )


def add_movies_to_user_list(user, movie_list, model_name):
    """
    This helper function adds the movies in movie_list
    to the list specified by model_name for the user.
    """
    users_list = getattr(user, model_name)
    movie_ids = [int(movie) for movie in movie_list]
    movie_models = Movie.objects.filter(pk__in=movie_ids)
    users_list.set(movie_models)


def get_random_movies(request):
    """
    This function returns a JSON response containing a list of random movies
    specified by the amount parameter in the GET request. It is used in
    the movie onboarding process.
    """
    amount = int(request.GET.get("amount", 25))
    movies = Movie.objects.order_by("?")[:amount]

    data = [
        {
            "id": movie.pk,
            "name": movie.name,
            "poster": movie.poster,
            "year": movie.year,
        }
        for movie in movies
    ]

    return JsonResponse({"movies": data})


def settings_view(request):
    return render(request, "accounts/profile_settings.html")


def preferences_movies_view(request):
    """
    This function handles the GET request for sending the user's movie preferences.
    """
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    if request.method != "GET":
        return HttpResponse(status=405)

    movies_liked = list(request.user.liked_films.all().values("pk", "poster", "name"))

    movies_disliked = list(
        request.user.disliked_films.all().values("pk", "poster", "name")
    )

    movies_watched = list(
        request.user.watched_films.all().values("pk", "poster", "name")
    )

    watchlist = list(request.user.watchlist_films.all().values("pk", "poster", "name"))
    # TODO uncomment when ready
    # movies_rewatch = list(
    #     request.user.films_to_rewatch.all().values("pk", "poster", "name")
    # )

    # movies_excluded = list(
    #     request.user.films_dont_recommend.all().values("pk", "poster", "name")
    # )

    movies_rewatch = []
    movies_excluded = []

    return JsonResponse(
        {
            "movies_liked": movies_liked,
            "movies_disliked": movies_disliked,
            "movies_watched": movies_watched,
            "watchlist": watchlist,
            "movies_rewatch": movies_rewatch,
            "movies_excluded": movies_excluded,
        }
    )


def onboarding_trigger_view(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    form = CustomTriggerForm()
    return render(
        request,
        "accounts/onboarding_triggers.html",
        {
            "form": form,
            "back_action": "redirectToOnboardingMovieForm()",
            "next_action": "submitOnboardingTriggerForm()",
            "back_text": "Back",
            "next_text": "Continue",
        },
    )
