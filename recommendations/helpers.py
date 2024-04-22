# TODO generic?
def recommendation_querying(recommendation, field, selection):
    # fields = recommendation._meta.get_fields()

    # # Print the field names and their values
    # for field in fields:
    #     field_name = field.name
    #     field_value = getattr(recommendation, field_name)
    #     print(f"{field_name}: {field_value}")
    if field != "triggers":
        return recommendation.possible_films.filter(**{f"{field}__contains": selection})

    return recommendation.possible_films.filter()
