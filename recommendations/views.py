import random

from django.conf import settings
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from ReeldIn.globals import ALL_MOVIES
from accounts.models import User


from .forms import *
from .helpers import (
    form_error_checking,
    make_new_recommendation,
    make_readable_recommendation,
    narrow_view_error,
    recommendation_querying,
    relevant_options,
    set_recommendation_attr,
    all_recommend,
    foreign_recommend,
)
from .models import Recommendation, RecentRecommendations

# starts at step 1 - for frontend to make sense
FORMS = ["", GenreForm, YearForm, RuntimeForm, LanguageForm, TriggerForm]
FIELD = ["", "Genres", "Years", "Runtimes", "Languages", "Triggers"]
MOVIE_MODEL_COMPLEMENT = ["", "genres", "year", "runtime", "language", "triggers"]


# user has requested to get a recommendation based on their inputs thus far OR has under ten options
def recommend_view(request):
    if request.user.is_authenticated is False:
        all_movies = ALL_MOVIES
        random_movies = random.sample(list(all_movies.all()), 3)
        readable_recommendation = make_readable_recommendation(random_movies)

        return render(
            request,
            "recommendations/recommendation.html",
            {"recommendations": readable_recommendation},
        )

    user = User.objects.get(username=request.user)
    recommendation = Recommendation.objects.get(user_id=user)

    # if user already has a recommendation generated, don't generate a new one
    if not recommendation.recommended_films.count():
        if recommendation.possible_film_count > 10:
            recommended_films = []
            possible_films = recommendation.possible_films

            check_triggers = False
            if recommendation.triggers and recommendation.triggers != [""]:
                check_triggers = True

            foreign_films = possible_films.exclude(language="en")
            foreign_recommend(
                recommended_films,
                possible_films,
                foreign_films,
                check_triggers,
                recommendation.triggers,
            )

            all_recommend(
                recommended_films,
                possible_films,
                check_triggers,
                recommendation.triggers,
            )

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

        # thanks for helping chatgpt
        recent_recs = all_recommended[:3] + list(all_recommendations.recent.all())[:27]
        with transaction.atomic():
            recommendation.possible_films.clear()
            all_recommendations.recent.clear()
            for film in recent_recs:
                all_recommendations.recent.add(film)

    readable_recommendation = make_readable_recommendation(
        recommendation.recommended_films.all()
    )

    package = {"recommendations": readable_recommendation}
    if recommendation.triggers != [""]:
        package["triggers"] = recommendation.triggers

    return render(request, "recommendations/recommendation.html", package)


# narrow the possible recommendations by querying based on submitted forms
def narrow_view(request):
    if request.user.is_authenticated is False:
        step = random.randint(1, len(FORMS) - 1)
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
        set_recommendation_attr(recommendation, selection, step=step)

        recommendation.save()

        form = FORMS[step + 1] if step + 1 < len(FORMS) else None

        # stop early or when no more questions remain
        if recommendation.possible_film_count < 10 or form is None:
            return recommend_view(request)

        if "Languages" in form.declared_fields:
            relevant_languages = relevant_options(
                form, recommendation.possible_films, recommendation.possible_film_count
            )

            # three languages + "No Preference"
            if len(relevant_languages) <= 4:
                recommendation.step += 1
                recommendation.save()

                form = FORMS[recommendation.step]
            else:
                form.declared_fields["Languages"].choices = relevant_languages

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

                package = {"recommendations": readable_recommendation}
                if recommendation.triggers != [""]:
                    package["triggers"] = recommendation.triggers

                return render(request, "recommendations/recommendation.html", package)
            else:
                step = recommendation.step
                form = FORMS[step] if step < len(FORMS) else None

                # shouldn't happen but just in case
                if recommendation.possible_film_count < 10 or form is None:
                    return recommend_view(request)

                # shouldn't be the languageForm() if three relevant languages
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
    new_recommendation = {"possible_film_count": 27122, "step": 1}

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        old_recommendation = Recommendation.objects.get(user_id=user)

        new_recommendation = make_new_recommendation(user, old_recommendation)

    return render(
        request,
        "recommendations/index.html",
        {"form": form, "recommendation": new_recommendation},
    )
