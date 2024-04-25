import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from recommendations.models import (
    Movie,
)
import random
from .forms import *
from .models import User, FriendRequest
import json

MOVIES_POST_TO_MODEL = {
    "movies_liked": "liked_films",
    "movies_disliked": "disliked_films",
    "movies_watched": "watched_films",
    "watchlist": "watchlist_films",
    "movies_rewatch": "rewatchable_films",
    "movies_blocked": "excluded_films",
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
                elif preference == "block":
                    blocked_genres.append(genre)
            with transaction.atomic():
                request.user.liked_genres = liked_genres
                request.user.disliked_genres = disliked_genres
                request.user.excluded_genres = blocked_genres
                request.user.save()
            return redirect("/accounts/onboarding/movies")
    else:
        # Fetch the user's preferences
        liked_genres = request.user.liked_genres
        disliked_genres = request.user.disliked_genres
        blocked_genres = request.user.excluded_genres

        # Prepare initial data dictionary for the form
        initial_data = {}
        for genre in GENRES:
            genre_value = genre[0]
            if genre_value in liked_genres:
                initial_data[genre_value] = "like"
            elif genre_value in disliked_genres:
                initial_data[genre_value] = "dislike"
            elif genre_value in blocked_genres:
                initial_data[genre_value] = "block"
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
    current_movies = set(users_list.values_list("id", flat=True))

    new_movie_set = set(movie_list)

    # TODO ideally do this before the POST on the client side
    movies_to_add = new_movie_set - current_movies
    movies_to_remove = current_movies - new_movie_set

    if movies_to_remove:
        users_list.remove(*Movie.objects.filter(id__in=movies_to_remove))
    if movies_to_add:
        users_list.add(*Movie.objects.filter(id__in=movies_to_add))


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
    movies_rewatch = list(
        request.user.rewatchable_films.all().values("pk", "poster", "name")
    )

    movies_excluded = list(
        request.user.excluded_films.all().values("pk", "poster", "name")
    )

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


# --- Friend handling begins ---


def send_friend_request(request):
    """
    This function handles when a user wants to send a friend request to another user.
    It returns the User object of the receiver if the request is successful.
    """

    # Check user is logged in
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    # Check request is POST and has username field
    if request.method != "POST":
        return redirect("landing_page:index")
    try:
        data = json.loads(request.body)
        request_username = data["username"]
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({"message": "Invalid JSON", "status": 400})

    # Invalid request handling
    try:
        receiver_user = User.objects.get(username=request_username)
    except User.DoesNotExist:
        return JsonResponse({"message": "User not found.", "status": 404})

    receiver_id = receiver_user.pk

    error_message = None
    status = 200
    if request.user.pk == receiver_id:
        error_message = "You can't send a friend request to yourself."
        status = 400
    elif request.user.friends.filter(pk=receiver_id).exists():
        error_message = "You are already friends with this user."
        status = 409
    elif FriendRequest.objects.filter(
        sender=request.user, receiver=receiver_user
    ).exists():
        error_message = "You have already sent a friend request to this user."
        status = 409
    elif FriendRequest.objects.filter(
        sender=receiver_user, receiver=request.user
    ).exists():
        error_message = ("You have already received a friend request from this user.",)
        status = 409

    if error_message is not None:
        return JsonResponse({"message": error_message}, status=status)
    # Create friend request
    with transaction.atomic():
        FriendRequest.objects.create(sender=request.user, receiver=receiver_user)
    print(receiver_user.profile_picture.url)
    return JsonResponse(
        {
            "message": "Friend request successfully sent!",
            "receiver": {
                "username": receiver_user.username,
                "profile_picture": receiver_user.profile_picture.url,
            },
        }
    )


def remove_friend(request):
    """
    This function handles when a user wants to remove a friend from their
    friends list.
    """

    # Check user is logged in
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    # Check request is POST and has username field
    if request.method != "POST":
        return redirect("landing_page:index")
    try:
        data = json.loads(request.body)
        request_username = data["username"]
    except (json.JSONDecodeError, KeyError):
        return HttpResponse("Invalid JSON", status=400)

    # Invalid request handling
    try:
        friend = User.objects.get(username=request_username)
    except User.DoesNotExist:
        return HttpResponse("User not found.", status=404)

    if not request.user.friends.filter(pk=friend.pk).exists():
        return HttpResponse("You are not friends with this user.", status=404)

    # Remove user from each others friends list
    with transaction.atomic():
        request.user.friends.remove(friend)
        friend.friends.remove(request.user)

    return HttpResponse("Successfully removed user from friends.", status=200)


def accept_friend_request(request):
    """
    This function handles when a user wants to accept a friend request they
    have received.
    """

    # Check user is logged in
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    # Check request is POST and has username field
    if request.method != "POST":
        return redirect("landing_page:index")
    try:
        data = json.loads(request.body)
        request_username = data["username"]
    except (json.JSONDecodeError, KeyError):
        return HttpResponse("Invalid JSON", status=400)

    # Error handling
    try:
        friend_request = FriendRequest.objects.get(
            sender=User.objects.get(username=request_username), receiver=request.user
        )
    except FriendRequest.DoesNotExist:
        return HttpResponse(
            "There is no friend request between you and this user.", status=404
        )

    # Handle friend request acceptance
    with transaction.atomic():
        request.user.friends.add(friend_request.sender)
        friend_request.sender.friends.add(request.user)
        friend_request.delete()

    return HttpResponse("Successfully accepted friend request.", status=200)


def delete_friend_request(request):
    """
    This function handles when a user either deletes a friend request they have sent,
    or rejects a friend request they have received.
    """
    # Check user is logged in
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    # Check request is POST and has necessary fields
    if request.method != "POST":
        return redirect("landing_page:index")
    try:
        data = json.loads(request.body)
        request_username = data["username"]
        username_is_sender = data["username_is_sender"]
    except (json.JSONDecodeError, KeyError):
        return HttpResponse("Invalid JSON", status=400)

    # Error handling
    try:
        if username_is_sender:
            friend_request = FriendRequest.objects.get(
                sender=User.objects.get(username=request_username),
                receiver=request.user,
            )
        else:
            friend_request = FriendRequest.objects.get(
                sender=request.user,
                receiver=User.objects.get(username=request_username),
            )
    except FriendRequest.DoesNotExist:
        return HttpResponse(
            "There is no friend request between you and this user.", status=404
        )

    # Delete friend request
    with transaction.atomic():
        friend_request.delete()

    return HttpResponse("Successfully deleted friend request.", status=200)
