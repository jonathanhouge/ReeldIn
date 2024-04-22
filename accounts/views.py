from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.db import transaction

from .forms import CustomUserCreationForm
from .models import User, FriendRequest
import json


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


def settings_view(request):
    return render(request, "accounts/profile_settings.html")


def onboarding(request):
    # if(request.session.get("onboarding")):
    return render(request, "accounts/onboarding.html")


# --- Friend request handling ---
def send_friend_request(request):
    print("send_friend_request called")
    if request.method != "POST":
        return redirect("landing_page:index")
    try:
        data = json.loads(request.body)  # Parsing JSON from the request body
        request_username = data["username"]  # Accessing the username field
    except (json.JSONDecodeError, KeyError):
        return HttpResponse("Invalid JSON", status=400)
    print("request_username: ", request_username)
    # Friend request error handling
    # user isn't logged in
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    # user doesn't exist
    try:
        receiver_user = User.objects.get(username=request_username)
    except User.DoesNotExist:
        return HttpResponse("User not found.", status=404)
    receiver_id = receiver_user.pk
    # user sends friend request to themselves
    if request.user.pk == receiver_id:
        return HttpResponse("You can't send a friend request to yourself.", status=400)
    # user is already friends with the other user
    if request.user.friends.filter(pk=receiver_id).exists():
        return HttpResponse("You are already friends with this user.", status=400)
    # user has already sent a friend request to the other user
    if FriendRequest.objects.filter(
        sender=request.user, receiver=receiver_user
    ).exists():
        return HttpResponse(
            "You have already sent a friend request to this user.", status=400
        )
    # user has already received a friend request from the other user
    if FriendRequest.objects.filter(
        sender=receiver_user, receiver=request.user
    ).exists():
        return HttpResponse(
            "You have already received a friend request from this user.", status=400
        )
    # create friend request
    with transaction.atomic():
        FriendRequest.objects.create(sender=request.user, receiver=receiver_user)
    return HttpResponse("Friend request sent.", status=200)


def remove_friend(request):
    print("remove_friend called")
    # Friend request error handling

    # request isn't POST or JSON is invalid
    if request.method != "POST":
        return redirect("landing_page:index")
    try:
        data = json.loads(request.body)  # Parsing JSON from the request body
        request_username = data["username"]  # Accessing the username field
    except (json.JSONDecodeError, KeyError):
        return HttpResponse("Invalid JSON", status=400)
    # user isn't logged in
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    # check if user exists
    try:
        friend = User.objects.get(username=request_username)
    except User.DoesNotExist:
        return HttpResponse("User not found.", status=404)
    # check if user is friends with the other user
    if not request.user.friends.filter(pk=friend.pk).exists():
        return HttpResponse("You are not friends with this user.", status=400)
    with transaction.atomic():
        request.user.friends.remove(friend)
        friend.friends.remove(request.user)
    return HttpResponse("Successfully removed user from friends.", status=200)


def accept_friend_request(request):
    if request.method != "POST":
        return redirect("landing_page:index")
    try:
        data = json.loads(request.body)  # Parsing JSON from the request body
        request_username = data["username"]  # Accessing the username field
    except (json.JSONDecodeError, KeyError):
        return HttpResponse("Invalid JSON", status=400)
    # Friend request error handling
    # user isn't logged in
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    try:
        friend_request = FriendRequest.objects.get(
            sender=User.objects.get(username=request_username), receiver=request.user
        )
    except FriendRequest.DoesNotExist:
        return HttpResponse("Friend request not found.", status=404)
    with transaction.atomic():
        request.user.friends.add(friend_request.sender)
        friend_request.sender.friends.add(request.user)
        friend_request.delete()
    return HttpResponse("Successfully accepted friend request.", status=200)


def decline_friend_request(request):
    if request.method != "POST":
        return redirect("landing_page:index")
    try:
        data = json.loads(request.body)  # Parsing JSON from the request body
        request_username = data["username"]  # Accessing the username field
    except (json.JSONDecodeError, KeyError):
        return HttpResponse("Invalid JSON", status=400)
    # Friend request error handling
    # user isn't logged in
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    try:
        friend_request = FriendRequest.objects.get(
            sender=User.objects.get(username=request_username), receiver=request.user
        )
    except FriendRequest.DoesNotExist:
        return HttpResponse("Friend request not found.", status=404)
    with transaction.atomic():
        friend_request.delete()
    return HttpResponse("Successfully rejected friend request.", status=200)


def delete_friend_request(request):
    if request.method != "POST":
        return redirect("landing_page:index")
    try:
        data = json.loads(request.body)  # Parsing JSON from the request body
        request_username = data["username"]  # Accessing the username field
    except (json.JSONDecodeError, KeyError):
        return HttpResponse("Invalid JSON", status=400)
    # Friend request error handling
    # user isn't logged in
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    try:
        friend_request = FriendRequest.objects.get(
            receiver=User.objects.get(username=request_username), sender=request.user
        )
    except FriendRequest.DoesNotExist:
        return HttpResponse("Friend request not found.", status=404)
    with transaction.atomic():
        friend_request.delete()
    return HttpResponse("Successfully deleted friend request.", status=200)
