import random
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from accounts.models import User

from .forms import *
from .helpers import recommendation_querying, make_new_recommendation
from .models import Movie, Recommendation

# starts at step 1 - for frontend to make sense
FORMS = ["", GenreForm, YearForm, RuntimeForm, LanguageForm, TriggerForm]
FIELD = ["", "Genres", "Years", "Runtimes", "Languages", "Triggers"]
MOVIE_MODEL_COMPLEMENT = ["", "genres", "year", "runtime", "language", "triggers"]
REC_ATTRIBUTE = ["", "genres", "year_span", "runtime_span", "languages", "triggers"]


# user has requested to get a recommendation based on their inputs thus far OR has under ten options
def recommend_view(request):
    if request.user.is_authenticated is False:
        all_movies = Movie.objects.all()
        random_movies = random.sample(all_movies, 3)
        return render(
            request,
            "recommendations/recommendation.html",
            {"recommendations": random_movies},
        )

    user = User.objects.get(username=request.user)
    recommendation = Recommendation.objects.get(user_id=user)

    recommendation.recommended_films.set(recommendation.possible_films)
    if recommendation.possible_film_count > 10:
        recommended_films = []
        possible_films = recommendation.recommended_films

        foreign_films = possible_films.exclude(language="en")
        while len(foreign_films):
            foreign_film = foreign_films[random.randint(0, len(foreign_films) - 1)]

            recommended_films.append(foreign_film)
            foreign_films.remove(foreign_film)
            possible_films.remove(foreign_film)

            if len(recommended_films) == 5:
                break

        while len(recommended_films) < 10:
            film = possible_films[random.randint(0, len(possible_films) - 1)]

            recommended_films.append(film)
            possible_films.remove(foreign_film)

        recommendation.recommended_films.set(recommended_films)

    recommendation.save()
    return render(
        request,
        "recommendations/recommendation.html",
        {"recommendations": recommendation.recommended_films},
    )


# narrow the possible recommendations by querying based on submitted forms
def narrow_view(request):
    if request.user.is_authenticated is False:
        step = random.randint(0, len(FORMS) - 1)
        form = FORMS[step]  # guests get to demo

        recommendation = {"possible_film_count": 27122, "step": step}
        return render(
            request,
            "recommendations/index.html",
            {"form": form, "recommendation": recommendation},
        )

    user = User.objects.get(username=request.user)
    recommendation = Recommendation.objects.get(user_id=user)
    step = recommendation.step

    form = FORMS[step](request.POST)
    if form.is_valid():
        field = FIELD[step]
        selection = form.cleaned_data.get(field, [])

        movies = recommendation_querying(
            recommendation, MOVIE_MODEL_COMPLEMENT[step], selection
        )
        recommendation.possible_films.set(movies)

        recommendation.possible_film_count = len(movies)
        recommendation.step += 1

        # sometimes an array, sometimes a string
        try:
            setattr(recommendation, REC_ATTRIBUTE[step], selection)
        except:
            setattr(recommendation, REC_ATTRIBUTE[step], selection[0])

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
        {"form": form, "error": form.errors, "recommendation": recommendation},
    )


def index(request):
    form = GenreForm()
    recommendation = {"possible_film_count": 27122, "step": 1}

    # if logged in, see if they have an ongoing, valid recommendation
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        try:
            recommendation = Recommendation.objects.get(user_id=user)
            if recommendation.step >= 20 or recommendation.possible_film_count < 10:
                recommendation.delete()

                recommendation = make_new_recommendation(user)
            else:
                form = FORMS[recommendation.step]

        except ObjectDoesNotExist:
            recommendation = make_new_recommendation(user)

    return render(
        request,
        "recommendations/index.html",
        {"form": form, "recommendation": recommendation},
    )
