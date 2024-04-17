from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .forms import CustomUserCreationForm
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
        providedUsername = request.POST["username"]
        providedPassword = request.POST["password"]
        user = authenticate(request, username=providedUsername, password=providedPassword)

        if user is not None:
            login(request, user)
            return redirect("landing_page:index")
        else:
            return render(
                request,
                "accounts/login.html",
                {"signInError": "Invalid username and/or password"},
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
            #request.session["onboarding"] = True TODO link to onboarding later
            #return render(request, "accounts/onboarding.html")
            return redirect("landing_page:index")
        # Else, determine error in signup and return message
        else:
            # checks if username is taken
            providedUsername = request.POST["username"]
            if User.objects.filter(username=providedUsername).exists():
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "signUpError": "Username has already been taken"},
                )
            # checks if email is taken
            providedEmail = request.POST["email"]
            if User.objects.filter(email=providedEmail).exists():
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "signUpError": "Email address is already in use"},
                )
            # checks if passwords match
            password1 = request.POST["password1"]
            confirm = request.POST["password2"]
            if password1 != confirm:
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "signUpError": "Passwords do not match"},
                )
            # if all else fails, return unknown error
            return render(
                request,
                "accounts/login.html",
                {"form": form, "signUpError": "An unknown error occured."},
            )
    elif request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "accounts/login.html", {"form": form})
    
def onboarding(request):
    #if(request.session.get("onboarding")):
    return render(request, "accounts/onboarding.html")