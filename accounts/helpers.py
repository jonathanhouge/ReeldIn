from recommendations.choices import GENRES
from recommendations.models import Movie


def add_movies_to_user_list(user, movie_list, model_name):
    """
    This helper function adds the movies in movie_list
    to the list specified by model_name for the user.
    """
    users_list = getattr(user, model_name)
    current_movies = set(users_list.values_list("id", flat=True))

    new_movie_set = set(movie_list)

    # TODO ideally do this before the POST on the client side
    movies_to_add = new_movie_set - current_movies
    movies_to_remove = current_movies - new_movie_set

    if movies_to_remove:
        users_list.remove(*Movie.objects.filter(id__in=movies_to_remove))
    if movies_to_add:
        users_list.add(*Movie.objects.filter(id__in=movies_to_add))


def get_user_genre_preferences(user):
    """
    Used in onboarding, returns current state of user genre preferences.
    """
    liked_genres = user.liked_genres
    disliked_genres = user.disliked_genres
    blocked_genres = user.excluded_genres

    initial_data = {}
    for genre in GENRES:
        genre_value = genre[0]
        if genre_value in liked_genres:
            initial_data[genre_value] = "like"
        elif genre_value in disliked_genres:
            initial_data[genre_value] = "dislike"
        elif genre_value in blocked_genres:
            initial_data[genre_value] = "block"
    return initial_data


def get_genre_form_data(form):
    liked_genres = []
    disliked_genres = []
    blocked_genres = []
    for genre, preference in form.cleaned_data.items():
        if preference == "like":
            liked_genres.append(genre)
        elif preference == "dislike":
            disliked_genres.append(genre)
        elif preference == "block":
            blocked_genres.append(genre)
    return liked_genres, disliked_genres, blocked_genres
