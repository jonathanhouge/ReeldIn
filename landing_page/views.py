import json
import os

import requests
from django.conf import settings
from django.core.serializers import serialize
from django.db.models import CharField, Q, TextField
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, redirect, render
from fuzzywuzzy import fuzz

from accounts.models import FriendRequest
from recommendations.choices import LANGUAGES
from recommendations.helpers import make_readable_recommendation
from recommendations.models import Movie, RecentRecommendations


def index(request):
    try:
        all_recommendations = RecentRecommendations.objects.get(id=1)
    except:
        all_recommendations = RecentRecommendations()
        all_recommendations.save()

    readable_recommendations = make_readable_recommendation(
        all_recommendations.recent.all()
    )

    return render(
        request,
        "landing_page/index.html",
        {"recommendations": readable_recommendations},
    )


def about(request):
    return render(request, "landing_page/about.html")


def contact(request):
    return render(request, "landing_page/contact.html")


def conditions(request):
    return render(request, "landing_page/conditions.html")


def error(request):
    return render(request, "landing_page/404.html")


def profile(request):
    if not request.user.is_authenticated:
        return render(request, "accounts/login.html")

    # Load context with user data
    recommended_movies = list(request.user.recommended_films.values("pk", "poster"))
    watched_movies = list(request.user.watched_films.values("pk", "poster"))
    liked_movies = list(request.user.liked_films.values("pk", "poster"))
    disliked_movies = list(request.user.disliked_films.values("pk", "poster"))
    watchlist_movies = list(request.user.watchlist_films.values("pk", "poster"))
    friends = request.user.friends.all()
    sent_requests = FriendRequest.objects.filter(sender=request.user)
    received_requests = FriendRequest.objects.filter(receiver=request.user)

    context = {
        "recommended_movies": recommended_movies,
        "watched_movies": watched_movies,
        "liked_movies": liked_movies,
        "disliked_movies": disliked_movies,
        "watchlist_movies": watchlist_movies,
        "friends": friends,
        "sent_requests": sent_requests,
        "received_requests": received_requests,
    }

    return render(request, "accounts/profile.html", context)
