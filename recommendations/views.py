from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from .models import Movie, Recommendation
from accounts.models import User
import random

FORMS = [GenreForm(), YearForm(), RuntimeForm(), TriggerForm()]
FIELD = ["Genres", "Years", "Runtimes", "Triggers"]


# user has requested to get a recommendation based on their inputs thus far OR has under ten options
def recommend_view(request):
    pass  # TODO


# narrow the possible recommendations by querying based on submitted forms
def narrow_view(request):
    form = GenreForm(request.POST)  # TODO generic

    # keep track of for logged in user, give a random joe any ol' form next (experience w/o actual rec)
    if form.is_valid() and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        recommendation = Recommendation.objects.get(user_id=user)
        step = recommendation.step
        selection = form.cleaned_data.get(FIELD[step], [])

        # first question will always be genre - populate possible films for the first time
        if step == 0:
            movies = Movie.objects.filter(genres__contains=selection)
        else:
            movies = recommendation.possible_films.filter(
                genres__contains=selection
            )  # TODO generic?
        print(movies)

        recommendation.possible_films.set(movies)
        recommendation.possible_film_count = len(movies)
        recommendation.step += 1

        recommendation.genres = selection  # TODO generic?
        recommendation.save()

        form = FORMS[step + 1]
        return render(
            request,
            "recommendations/index.html",
            {"form": form},
        )
    elif form.is_valid() and request.user.is_authenticated is False:
        form = FORMS[random.randint(0, len(FORMS) - 1)]
        return render(
            request,
            "recommendations/index.html",
            {"form": form},
        )

    # form was invalid
    return render(request, "dashboard/404.html")  # TODO implement punishment


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
