import random

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from accounts.models import User

from .forms import *
from .helpers import (
    form_error_checking,
    make_new_recommendation,
    make_readable_recommendation,
    narrow_view_error,
    recommendation_querying,
    relevant_options,
)
from .models import Movie, Recommendation, RecentRecommendations

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

    # if user already has a recommendation generated, don't generate a new one
    if not recommendation.recommended_films.count():
        if recommendation.possible_film_count > 10:
            recommended_films = []
            possible_films = recommendation.possible_films

            foreign_films = possible_films.exclude(language="en")
            while foreign_films.count():
                pks = foreign_films.values_list("pk", flat=True)
                random_pk = random.choice(pks)
                foreign_film = foreign_films.get(pk=random_pk)

                recommended_films.append(foreign_film)
                foreign_films = foreign_films.exclude(id=foreign_film.id)
                possible_films = possible_films.exclude(id=foreign_film.id)

                if len(recommended_films) == 3:
                    break  # ensure at least three non-english films

            while len(recommended_films) < 10 or possible_films.count() == 0:
                pks = possible_films.values_list("pk", flat=True)
                random_pk = random.choice(pks)
                film = possible_films.get(pk=random_pk)

                recommended_films.append(film)
                possible_films = possible_films.exclude(id=film.id)

            recommendation.recommended_films.set(recommended_films)
        else:
            recommendation.recommended_films.set(recommendation.possible_films.all())

        recommendation.save()

        # update user's recommended and site-wide recommended
        already_recommended = list(user.recommended_films.all())
        all_recommended = list(recommendation.recommended_films.all())
        user.recommended_films.set(already_recommended + all_recommended)

        try:
            all_recommendations = RecentRecommendations.objects.get(id=1)
        except:
            all_recommendations = RecentRecommendations()  # should exist, just in case
            all_recommendations.save()

        recent_recs = list(all_recommendations.recent.all())[:27]
        all_recommendations.recent.set(all_recommended[:3] + recent_recs)

    readable_recommendation = make_readable_recommendation(
        recommendation.recommended_films.all()
    )

    return render(
        request,
        "recommendations/recommendation.html",
        {"recommendations": readable_recommendation},
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

    form = FORMS[step](request.POST) if step < len(FORMS) else None
    if form is None:
        return recommend_view(request)  # weird bug i got once - counters it

    if form.is_valid():
        field = FIELD[step]
        selection = form.cleaned_data.get(field, [])
        filter_method = form.cleaned_data.get("Filters", "")

        error_message = form_error_checking(field, selection)
        if error_message:
            return narrow_view_error(request, form, error_message, recommendation)

        movies = recommendation_querying(
            recommendation, MOVIE_MODEL_COMPLEMENT[step], selection, filter_method
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

        # stop early or when no more questions remain
        if recommendation.possible_film_count < 10 or form is None:
            return recommend_view(request)

        if "Languages" in form.declared_fields:
            form.declared_fields["Languages"].choices = relevant_options(
                form, recommendation.possible_films, recommendation.possible_film_count
            )

        return render(
            request,
            "recommendations/index.html",
            {"form": form, "recommendation": recommendation},
        )

    if settings.DEBUG:
        print(form.errors)

    # form was invalid, give them the same form
    form = FORMS[step]
    return narrow_view_error(
        request,
        form,
        "Error: Try again. Maybe you didn't make a selection? If this persists, contact the devs.",
        recommendation,
    )


def index(request):
    form = FORMS[1]  # GenreForm()
    recommendation = {"possible_film_count": 27122, "step": 1}

    # if logged in, see if they have an ongoing, valid recommendation
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)

        try:
            recommendation = Recommendation.objects.get(user_id=user)

            if recommendation.recommended_films.count():
                readable_recommendation = make_readable_recommendation(
                    recommendation.recommended_films.all()
                )

                return render(
                    request,
                    "recommendations/recommendation.html",
                    {"recommendations": readable_recommendation},
                )
            else:
                step = recommendation.step
                form = FORMS[step] if step < len(FORMS) else None

                # shouldn't happen but just in case
                if recommendation.possible_film_count < 10 or form is None:
                    return recommend_view(request)

                if "Languages" in form.declared_fields:
                    form.declared_fields["Languages"].choices = relevant_options(
                        form,
                        recommendation.possible_films,
                        recommendation.possible_film_count,
                    )

        except ObjectDoesNotExist:
            recommendation = make_new_recommendation(user)

    return render(
        request,
        "recommendations/index.html",
        {"form": form, "recommendation": recommendation},
    )


def delete_view(request):
    form = GenreForm()
    recommendation = {"possible_film_count": 27122, "step": 1}

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        recommendation = Recommendation.objects.get(user_id=user)
        recommendation.delete()

        recommendation = make_new_recommendation(user)

    return render(
        request,
        "recommendations/index.html",
        {"form": form, "recommendation": recommendation},
    )
