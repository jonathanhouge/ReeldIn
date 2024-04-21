# TODO generic?
def recommendation_querying(recommendation, selection):
    movies = recommendation.possible_films.filter(genres__contains=selection)
