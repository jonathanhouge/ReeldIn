import random
import re

import django.http
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from accounts.models import User

from .forms import *
from .helpers import recommendation_querying
from .models import Movie, Recommendation

FORMS = [GenreForm, YearForm, RuntimeForm, TriggerForm]
FIELD = ["Genres", "Years", "Runtimes", "Triggers"]
FIELD_DICT = {
    "Genres": "genres",
    "Years": "year",
    "Runtimes": "runtime",
    "Triggers": "triggers",
}


# user has requested to get a recommendation based on their inputs thus far OR has under ten options
def recommend_view(request):
    pass  # TODO


# narrow the possible recommendations by querying based on submitted forms
# TODO more than just genres (generic problems)
def narrow_view(request):
    if request.user.is_authenticated is False:
        form = FORMS[random.randint(0, len(FORMS) - 1)]  # guests get to test
        return render(
            request,
            "recommendations/index.html",
            {"form": form},
        )

    user = User.objects.get(username=request.user)
    recommendation = Recommendation.objects.get(user_id=user)
    step = recommendation.step

    form = FORMS[step](request.POST)

    if form.is_valid():
        field = FIELD[step]
        selection = form.cleaned_data.get(field, [])

        # first question will always be genre - populate possible films for the first time
        if step == 0:
            movies = Movie.objects.filter(genres__contains=selection)
        else:
            movies = recommendation_querying(
                recommendation, FIELD_DICT[field], selection
            )

        recommendation.possible_films.set(movies)
        recommendation.possible_film_count = len(movies)
        recommendation.step += 1

        recommendation.genres = selection  # TODO generic?
        recommendation.save()

        form = FORMS[step + 1] if step + 1 < len(FORMS) else None
        return render(
            request,
            "recommendations/index.html",
            {"form": form, "recommendation": recommendation},
        )

    # form was invalid, give them the same form
    form = FORMS[step]
    return render(
        request,
        "recommendations/index.html",
        {"form": form, "error": form.errors},
    )


def index(request):
    form = GenreForm()

    # if logged in, see if they have an ongoing, valid recommendation
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        try:
            recommendation = Recommendation.objects.get(user_id=user)
            if recommendation.step >= 20 or recommendation.possible_film_count < 10:
                recommendation.delete()

                recommendation = Recommendation(user_id=user)
                recommendation.save()
            else:
                form = FORMS[recommendation.step]

        except ObjectDoesNotExist:
            recommendation = Recommendation(user_id=user)
            recommendation.save()

    return render(
        request,
        "recommendations/index.html",
        {"form": form},
    )
