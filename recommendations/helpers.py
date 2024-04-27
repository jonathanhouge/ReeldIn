from django.conf import settings
from django.db.models import Count
from django.shortcuts import render

from .choices import LANGUAGES
from .models import Movie, Recommendation


# creates a new recommendation model and sets it up
def make_new_recommendation(user):
    recommendation = Recommendation(user_id=user)
    recommendation.save()  # needs id

    all_movies = Movie.objects.all()
    recommendation.possible_films.set(all_movies)
    recommendation.possible_film_count = len(all_movies)
    recommendation.save()
    return recommendation


# makes sure the user only sees relevant options (only for languages so far)
# note: chatgpt helped make this way more efficient - was querying the db too much
def relevant_options(form, possible_films, possible_films_count):
    relevant_languages = [form.OPTIONS[0]]  # always have 'no preference'
    films_covered = 0

    # Annotate the queryset with the count of films for each language
    annotated_films = possible_films.values("language").annotate(num_films=Count("id"))

    for language_code, language_name in form.OPTIONS:
        # Find the count of films for the current language
        language_count = next(
            (
                entry["num_films"]
                for entry in annotated_films
                if entry["language"] == language_code
            ),
            0,
        )

        if language_count:
            relevant_languages.append((language_code, language_name))
            films_covered += language_count

        if films_covered == possible_films_count:
            break  # stop early if possible

    return relevant_languages


# works for genre, year, runtime, language
def recommendation_querying(recommendation, field, selection, filter):
    if ("" in selection and isinstance(selection, list)) or len(selection) == 0:
        return recommendation.possible_films.all()  # user has no pref

    if field == "year" or field == "runtime":
        span = selection.split("-")
        return recommendation.possible_films.filter(
            **{f"{field}__gte": span[0]}, **{f"{field}__lte": span[1]}
        )
    elif field == "language":
        return recommendation.possible_films.filter(language__in=selection)
    elif field == "genres":
        if filter == "Or":
            possible_movies = Movie.objects.none()
            for genre in selection:
                possible_movies |= recommendation.possible_films.filter(
                    genres__contains=[genre]
                )

            return possible_movies
        return recommendation.possible_films.filter(**{f"{field}__contains": selection})

    if settings.DEBUG:
        print(
            f"How did you get here? Here's what I have for everything: {recommendation.__dict__}, {field}, {selection}, {filter}"
        )

    return recommendation.possible_films.all()  # prevent rec from being broken


# make arrays strings, make choices human readable, etc.
def make_readable_recommendation(recommended_films):
    readable_recommendation = []
    for film in recommended_films:
        readable_film = {
            "id": film.id,
            "name": film.name,
            "poster": film.poster,
            "year": film.year,
            "language": "",
            "genre": "",
            "director": "",
        }

        language_dict = dict(LANGUAGES)  # thanks chatgpt
        readable_film["language"] = language_dict.get(film.language)

        readable_film["genres"] = (", ").join(film.genres)
        readable_film["director"] = (", ").join(film.director)

        readable_recommendation.append(readable_film)

    return readable_recommendation


# if we have any requirements that django wouldn't normally catch
def form_error_checking(field, selection):
    if field == "Languages" and (len(selection) < 3 and "" not in selection):
        return "You must pick at least three languages. If there are less than three, select 'No Preference'."

    return ""


# since we return this in two place, i made a function to avoid code duplication
def narrow_view_error(request, form, message, recommendation):
    return render(
        request,
        "recommendations/index.html",
        {
            "form": form,
            "error": message,
            "recommendation": recommendation,
        },
    )
