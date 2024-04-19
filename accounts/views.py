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
                {"signin_error": "Invalid username and/or password"},
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
        # If signup valid, log user in and redirect to onboarding
        if form.is_valid():
            user = form.save()
            login(request, user)
            # request.session["onboarding"] = True TODO link to onboarding later
            # return render(request, "accounts/onboarding.html")
            return redirect("landing_page:index")
        # Else, determine error in signup and return message
        else:
            # checks if username is taken
            provided_username = request.POST["username"]
            if User.objects.filter(username=provided_username).exists():
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "signup_error": "Username has already been taken"},
                )
            # checks if email is taken
            providedEmail = request.POST["email"]
            if User.objects.filter(email=providedEmail).exists():
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "signup_error": "Email address is already in use"},
                )
            # checks if passwords match
            password1 = request.POST["password1"]
            confirm = request.POST["password2"]
            if password1 != confirm:
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "signup_error": "Passwords do not match"},
                )
            # if all else fails, return unknown error
            return render(
                request,
                "accounts/login.html",
                {"form": form, "signup_error": "An unknown error occured."},
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
    if request.method == "POST":
        form = GenreForm(request.POST)
        # TODO populate with user preferences (here or in forms.py)
        if form.is_valid():
            # TODO Process the form data
            return redirect("/accounts/onboarding/movies")
    else:
        form = GenreForm()
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


# TODO back_action does not redirect to home page


def onboarding_movie_view(request):
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


def get_random_movies(request):
    amount = int(request.GET.get("amount", 25))
    movies = list(Movie.objects.all())
    random.shuffle(movies)
    movies = movies[:amount]

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
