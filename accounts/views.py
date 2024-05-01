import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from recommendations.models import Movie
from recommendations.choices import STREAMING, TRIGGERS
from fuzzywuzzy import fuzz

from .forms import CustomUserCreationForm, GenreForm, CustomBooleanForm
from .models import User, FriendRequest
import json
from .helpers import (
    get_user_genre_preferences,
    add_movies_to_user_list,
    get_genre_form_data,
)
import csv

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
            # onboarding set to true so final page redirects to recommendations
            request.session["onboarding"] = True
            return render(request, "accounts/onboarding.html")
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


def onboarding_view(request):
    """
    The intro page is only visible to users who have just signed up.
    """
    if request.session.get("onboarding"):
        return render(
            request,
            "accounts/onboarding.html",
        )
    return redirect("landing_page:index")


def onboarding_genre_view(request):
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
            return redirect("/accounts/onboarding/imports/")
    else:
        initial_data = get_user_genre_preferences(request.user)
        form = GenreForm(initial_preferences=initial_data)
    return render(request, "accounts/onboarding_genres.html", {"form": form})


def onboarding_movie_view(request):
    """
    This function handles the POST/GET requests for the onboarding movie form.
    POST saves the user's preferences while GET renders the page.
    """
    if request.method != "POST":
        return render(
            request,
            "accounts/onboarding_movies.html",
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

    # TODO ideally do this before the POST on the client side
    movies_to_add = new_movie_set - current_movies
    movies_to_remove = current_movies - new_movie_set

    if movies_to_remove:
        users_list.remove(*Movie.objects.filter(id__in=movies_to_remove))
    if movies_to_add:
        users_list.add(*Movie.objects.filter(id__in=movies_to_add))


def onboarding_import_view(request):
    return render(request, "accounts/onboarding_imports.html")


# Sends file to either IMDb or Letterboxd data handling functions
def onboarding_upload(request):
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


# For testing purposes
# add this button to profile.html
# <button onclick="clearLists()">Clear Lists</button>
def clear_lists(request):
    user = request.user
    with transaction.atomic():
        user.liked_films.clear()
        user.disliked_films.clear()
        user.watched_films.clear()
        user.watchlist_films.clear()
        user.rewatchable_films.clear()
        user.excluded_films.clear()
    user.watched_films.add(Movie.objects.get(imdb_id="tt0137523"))
    return HttpResponse("Lists cleared", status=200)


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

            return redirect("/accounts/onboarding/streaming")
    else:
        initial_data = {trigger: True for trigger in user.triggers}
        form = CustomBooleanForm(items=TRIGGERS, initial_preferences=initial_data)
    return render(request, "accounts/onboarding_triggers.html", {"form": form})


def onboarding_streaming_view(request):

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
                return redirect("recommendations:recommendations")
            return redirect("accounts:settings")
    else:
        initial_data = {service: True for service in user.subscriptions}
        form = CustomBooleanForm(items=STREAMING, initial_preferences=initial_data)
    return render(request, "accounts/onboarding_streaming.html", {"form": form})


def sort_by_closeness(query, movie):
    return fuzz.ratio(query, movie.name)


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
                "id": movie.pk,  # TODO id?
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


def change_username(request):
    data = json.loads(request.body)
    print(data)
    username = data.get("username")
    if username:
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)
        else:
            request.user.username = username
            request.user.save()
            return JsonResponse(
                {"success": "Username changed successfully"}, status=200
            )
    else:
        return JsonResponse({"error": "Username cannot be blank"}, status=400)


def change_password(request):
    print("Change password")
    data = json.loads(request.body)
    password = data.get("password")
    if password is not None:
        request.user.set_password(password)
        return HttpResponse("Change username", status=200)
    else:
        return HttpResponse("Cannot be blank", status=400)


def delete_account(request):
    print("Delete account")
    request.user.delete()
    return HttpResponse("Delete account", status=200)
