from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from .models import Movie, Recommendation
import random

FORMS = [GenreForm(), YearForm(), RuntimeForm(), TriggerForm()]
FIELD = ["Genres", "Years", "Runtimes", "Triggers"]


def recommend_view(request):
    form = GenreForm(request.POST)  # TODO generic

    # keep track of for logged in user, give a random joe any ol' form next (experience w/o actual rec)
    if form.is_valid() and request.user.is_authenticated:
        recommendation = Recommendation.objects.filter(id=request.user)
        step = recommendation.step
        selection = form.cleaned_data.get(FIELD[step], [])

        movies = []
        if step == 0:
            movies = Movie.objects.filter(genres=selection)
        else:
            movies = recommendation.movies.filter(field=selection)  # TODO generic

        recommendation.movies = movies
        recommendation.possible_film_count = len(movies)
        recommendation.step += 1
        recommendation.genres = selection  # TODO generic

        Recommendation.save()

        form = FORMS[step + 1]
        return render(
            request,
            "recommendations/index.html",
            {"form": form},
        )
    elif form.is_valid() and request.user.is_athenticated is False:
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
    if request.user.is_authenticated:
        try:
            recommendation = Recommendation.objects.get(id=request.user)
            if recommendation.step >= 20 or recommendation.possible_film_count < 10:
                recommendation.delete()

                recommendation = Recommendation(user=request.user)
                recommendation.save()
            else:
                form = FORMS[recommendation.step]

        except ObjectDoesNotExist:
            print("User wasn't mid-rec.")

            recommendation = Recommendation(user=request.user)
            recommendation.save()

    return render(
        request,
        "recommendations/index.html",
        {"form": form},
    )
