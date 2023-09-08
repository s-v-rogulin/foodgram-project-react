def get_queryset_filter(queryset, user, value, relation):
    if user.is_anonymous:
        return queryset
    if bool(value):
        return queryset.filter(**{relation: user})
    return queryset.exclude(**{relation: user})
