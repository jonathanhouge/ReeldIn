# TODO only works for genre, year, runtime
def recommendation_querying(recommendation, field, selection):
    if field == "year" or field == "runtime":
        span = selection.split("-")
        print(span)
        return recommendation.possible_films.filter(
            **{f"{field}__gte": span[0]}, **{f"{field}__lte": span[1]}
        )

    # genre
    return recommendation.possible_films.filter(**{f"{field}__contains": selection})
