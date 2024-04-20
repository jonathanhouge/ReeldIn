from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .forms import CustomUserCreationForm
from .models import User, FriendRequest


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


# Friend request handling
def send_friend_request(request, username):
    # Friend request error handling

    # user doesn't exist
    try:
        receiver_user = get_object_or_404(User, username=username)
    except User.DoesNotExist:
        return HttpResponse("User not found.")
    receiver_id = receiver_user.pk
    # user sends friend request to themselves
    if request.user.pk == receiver_id:
        return HttpResponse("You can't send a friend request to yourself.")
    # user is already friends with the other user
    if request.user.friends.filter(pk=receiver_id).exists():
        return HttpResponse("You are already friends with this user.")
    # user has already sent a friend request to the other user
    if FriendRequest.objects.filter(
        sender=request.user, receiver=receiver_user
    ).exists():
        return HttpResponse("You have already sent a friend request to this user.")
    # user has already received a friend request from the other user
    if FriendRequest.objects.filter(
        sender__pk=receiver_id, receiver=request.user
    ).exists():
        return HttpResponse(
            "You have already received a friend request from this user."
        )
    FriendRequest.objects.create(sender=request.user, receiver=receiver_id)
    return redirect("accounts:profile")  # TODO redirect ?


def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(
        FriendRequest, pk=request_id, receiver=request.user
    )
    friend_request.status = "accepted"
    friend_request.save()
    # Optionally add to each user's friend list
    request.user.friends.add(friend_request.sender)
    friend_request.sender.friends.add(request.user)
    return redirect("accounts:profile")  # TODO redirect ?


def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(
        FriendRequest, pk=request_id, receiver=request.user
    )
    friend_request.status = "declined"
    friend_request.save()
    return redirect("accounts:profile")  # TODO redirect ?


def get_sent_friend_requests(request):
    sent_requests = FriendRequest.objects.filter(sender=request.user)
    return render(  # TODO make this just return a json
        request, "accounts/sent_friend_requests.html", {"sent_requests": sent_requests}
    )


def get_pending_friend_requests(request):
    pending_requests = FriendRequest.objects.filter(
        receiver=request.user, status="pending"
    )
    return render(  # TODO make this just return a json
        request,
        "accounts/pending_friend_requests.html",
        {"pending_requests": pending_requests},
    )
