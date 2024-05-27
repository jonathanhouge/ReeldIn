from django.shortcuts import render, redirect


# Create your views here.
def is_admin(user):
    return user.is_superuser


def index(request):

    # if user is not logged in, redirect to home page
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    return render(request, "dashboard/index.html")
